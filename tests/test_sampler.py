from tempfile import NamedTemporaryFile as temp
from datetime import datetime as dt
from unittest import TestCase

from sampler import Sampler
from friskby_dao import FriskbyDao
from serial import SerialException

try:
    from sds011 import SDS011
except SerialException:
    from mock_sds011 import SDS011


class SamplerTest(TestCase):

    def setUp(self):
        tmpf = temp(delete=False)
        self.fname = tmpf.name + '_db.sql'
        tmpf.close()
        self.dao = FriskbyDao(self.fname)

    def test_sampler(self):
        sample_time = 2
        sleep_time = 0.10

        start = dt.now()
        sampler = Sampler(SDS011(True), self.dao, sample_time=sample_time, sleep_time=sleep_time)
        sampler.collect()
        stop = dt.now()

        delta = stop - start
        self.assertTrue((delta.total_seconds() - sample_time) > 0)
        data = self.dao.get_non_uploaded(limit=30)
        self.assertTrue(len(data) > 0)
