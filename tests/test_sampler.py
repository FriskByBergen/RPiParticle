import tempfile 
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
        with self.assertRaises(ValueError):
            sampler = Sampler( SDS011(true) )

        with self.assertRaises(ValueError):
            sampler = Sampler( SDS011(true) , num_sample = 100)

        with self.assertRaises(ValueError):
            sampler = Sampler( SDS011(true) , num_sample = 100, sleep_time = 10 , sample_time = 100)

        with self.assertRaises(ValueError):
            sampler = Sampler( SDS011(true) , sample_time = 10 , sleep_time = 100)
        
        sampler = Sampler( SDS011(true) , sample_time = 1 , num_sample = 10 )
        data = sampler.collect( )
        for x in data:
            self.assertEqual( len(x) , 10 )
    
