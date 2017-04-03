from unittest import TestCase
from random import randint

from friskby import TS, FriskbyDao, FriskbySampler

class MockSDS011(object):
    def __init__(self, device_url):
        self.device_url = device_url
    def read(self):
        return (10.0, 2.5)

class FriskbyIntegration(TestCase):

    def test_ts(self):
        t = TS()
        t.append(4)
        t.append(6)
        self.assertEqual(5.0, t.mean())

    def test_dao_sampler(self):
        dao_sql_fname = '/tmp/rpiparticle/%d__.sql' % randint(2**42, 2**52)
        dao = FriskbyDao(dao_sql_fname)
        sampler = FriskbySampler(MockSDS011('/path/to/dev'), dao,
                                 sample_time=0.1, sleep_time=0.1)
        sampler.collect()
        data = dao.get_non_uploaded(limit=30)
        self.assertTrue(len(data) > 0)
