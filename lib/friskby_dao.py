import json
import sqlite3
from os.path import isfile, abspath

class FriskbyDao(object):
    """A very simple access object to the samples.
    Uses sqlite3 to persist sample data.  Available functions:
    
    1. persist(data)    --- store sampled values
    2. rows(limit=100)  --- get limit number of non-uploaded rows
    3. cleanup()        --- drop uploaded 
    4. update(data,upl) --- set corresponding rows as uploaded

    Needs a configuration object to get db_path and db_name.
    """

    def __init__(self, conf):
        path = conf['db_path']
        path = abspath(path)
        if not isfile(path):
            raise IOError('Provided DB "%s" is not a file.' % path)
        self.__conn = sqlite3.connect(path)
        self._db_name = conf['db_name']

    def cleanup(self):
        self.__conn.execute('DROP * FROM %s WHERE UPLOADED' % self._db_name)

    def persist(self, data):
        pass

    def rows(self, limit = 100, uploaded = False):
        pass

    def update(self, data, uploaded = True):
        pass

