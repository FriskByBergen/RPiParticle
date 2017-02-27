from tempfile import NamedTemporaryFile as temp
from unittest import TestCase
from random import random as rnd
import sqlite3
from datetime import datetime as dt
from ts import TS
from friskby_dao import FriskbyDao

def rand():
    return round(rnd()*100, 2)

def gen_rand_ts():
    t = TS()
    for _ in range(3):
        t.append(rand())
    return t

class DaoTest(TestCase):

    def setUp(self):
        tmpf = temp(delete=False)
        self.fname = tmpf.name + '_db.sql'
        tmpf.close()
        self.dao = FriskbyDao(self.fname)

    def test_created(self):
        q = "SELECT name FROM sqlite_master WHERE type='table';"
        conn = sqlite3.connect(self.fname)
        c = conn.execute(q)
        result = c.fetchall()
        self.assertEqual(1, len(result))
        self.assertEqual('samples', result[0][0])

    def _do_test_num_upl(self, dao, exp_num_all, exp_num_upl, exp_num_nup):
        num_all, num_upl, num_nup = (dao.get_num_rows(),
                                     dao.get_num_rows(uploaded_status=True),
                                     dao.get_num_rows(uploaded_status=False))
        self.assertEqual(exp_num_all, num_all)
        self.assertEqual(exp_num_upl, num_upl)
        self.assertEqual(exp_num_nup, num_nup)

    def test_persist(self):
        num_data = 13
        for _ in range(num_data):
            t10 = gen_rand_ts()
            t25 = gen_rand_ts()
            self.dao.persist_ts((t10, t25))

        self._do_test_num_upl(self.dao, 2*num_data, 0, 2*num_data)

        data = self.dao.get_non_uploaded(limit=30)
        self.assertEqual(2*num_data, len(data))

    def test_mark_uploaded(self):
        num_data = 17
        for _ in range(num_data):
            t10 = gen_rand_ts()
            t25 = gen_rand_ts()
            self.dao.persist_ts((t10, t25))
        print(repr(self.dao))

        self._do_test_num_upl(self.dao, 2*num_data, 0, 2*num_data)

        data = self.dao.get_non_uploaded(limit=30)
        self.assertEqual(30, len(data))
        self.dao.mark_uploaded(data)
        data = self.dao.get_non_uploaded(limit=30)
        self.assertEqual(4, len(data)) # total 34, marked 30
        print(repr(self.dao))

        # test num / num upl / num non-upl
        self._do_test_num_upl(self.dao, 2*num_data, 30, 2*num_data - 30)

    def test_localtime(self):
        t10 = gen_rand_ts()
        t25 = gen_rand_ts()
        now = dt.now()
        self.dao.persist_ts((t10, t25))
        out = self.dao.get_non_uploaded(limit=1)[0]
        delta = now - out[3]
        # checking that we're in the same timezone
        self.assertTrue(abs(delta.total_seconds()) < 1000)
