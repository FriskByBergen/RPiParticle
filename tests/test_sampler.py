import tempfile 
import datetime
from unittest import TestCase
import os.path
import stat
from sampler import Sampler

from serial import SerialException

try:
    from sds011 import SDS011
except SerialException:
    from mock_sds011 import SDS011


class SamplerTest(TestCase):

    def test_sampler(self):
        sample_time = 2
        sleep_time = 0.10

        start = datetime.datetime.now()
        sampler = Sampler( SDS011(True) , sample_time = sample_time , sleep_time = sleep_time )
        data = sampler.collect( )
        stop = datetime.datetime.now( )
        
        dt = stop - start
        self.assertTrue( (dt.total_seconds() - sample_time) <= 2*sleep_time )
        
