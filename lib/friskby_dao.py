import sys
from sys import stderr, argv
from os.path import abspath, isfile
import sqlite3
from datetime import datetime as dt
from dateutil import parser as dt_parser

def _insert(val, sensor):
    """Returns INSERT query"""
    query = "INSERT INTO samples (id, value, sensor, timestamp) VALUES (NULL, %f, '%s', '%s');"
    return query % (val, sensor, dt.utcnow())

class FriskbyDao(object):

    def __init__(self, sql_path):
        """The sqlite db has a table called 'samples' with schema
        id, value, sensor, timestamp, uploaded
        """
        self._sql_path = abspath(sql_path)
        self.__init_sql()

    def get_path(self):
        return self._sql_path

    def __init_sql(self):
        if not isfile(self._sql_path):
            _id = '`id` INTEGER PRIMARY KEY'
            _val = '`value` FLOAT NOT NULL'
            _sen = '`sensor` TEXT NOT NULL'
            _date = '`timestamp` TEXT NOT NULL'
            _upl = '`uploaded` BOOL DEFAULT 0'
            _create = 'CREATE TABLE samples (%s, %s, %s, %s, %s);'
            schema = _create % (_id, _val, _sen, _date, _upl)
            conn = sqlite3.connect(self._sql_path)
            conn.execute(schema)
            conn.close()

    def get_num_rows(self, uploaded_status=None):
        """Gets num rows in sql storage.  If uploaded_status is set to True, we
        fetch number of rows that are marked uploaded, if uploaded_status is set
        to False, we fetch number of rows that are marked as not uploaded.
        """
        query = 'SELECT COUNT(uploaded) FROM samples'
        if uploaded_status is not None:
            if uploaded_status:
                query += ' WHERE uploaded'
            else:
                query += ' WHERE NOT uploaded'
        query += ';'
        conn = sqlite3.connect(self._sql_path)
        result = conn.execute(query)
        num = result.fetchone()[0]
        conn.close()
        return num


    def get_non_uploaded(self, limit=100):
        sub_q = "id, value, sensor, datetime(timestamp, 'localtime'), uploaded"
        query = 'SELECT %s FROM samples WHERE NOT `uploaded` LIMIT %d;'
        try:
            conn = sqlite3.connect(self._sql_path)
            result = conn.execute(query % (sub_q, limit))
            data = result.fetchall()
            conn.close()
            print('dao fetched %d rows of non-uploaded data' % len(data))
            sys.stdout.flush()
            for i in range(len(data)):
                id_, val_, sens_, dt_, upl_ = data[i]
                data[i] = id_, val_, sens_, dt_parser.parse(dt_), upl_
            return data
        except Exception as err:
            stderr.write('Error on reading data: %s.\n' % err)

    def persist_ts(self, data):
        ts_pm10, ts_pm25 = data
        q10 = _insert(ts_pm10.median(), 'PM10')
        q25 = _insert(ts_pm25.median(), 'PM25')
        try:
            conn = sqlite3.connect(self._sql_path)
            conn.execute(q10)
            conn.execute(q25)
            conn.commit()
            conn.close()
        except Exception as err:
            stderr.write('Error on persisting data: %s.\n' % err)
        print('Persisted data.')
        sys.stdout.flush()

    def mark_uploaded(self, data):
        print('dao marking ...')
        sys.stdout.flush()
        query = 'UPDATE samples SET uploaded=1 WHERE id=%s'
        try:
            conn = sqlite3.connect(self._sql_path)
            conn.execute('begin')
            for row in data:
                # id, value, sensor, timestamp, uploaded
                id_ = row[0]
                conn.execute(query % id_)
            conn.commit()
            conn.close()
        except Exception as err:
            stderr.write('Error on setting UPLOADED data! %s.\n' % err)


    def __repr__(self):
        try:
            num, num_up = self.get_num_rows(), self.get_num_rows(uploaded_status=True)
            fmt = 'FriskbyDao(num_rows = %s, non_uploaded = %s, path = %s)'
            return fmt % (num, num_up, self._sql_path)
        except:
            return 'FriskbyDao(path = %s)' % (self._sql_path)

if __name__ == '__main__':
    if len(argv) > 1:
        FriskbyDao(argv[1])
