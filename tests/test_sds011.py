import tempfile 
from unittest import TestCase, skipUnless, skipIf
import os.path
import stat
from serial import SerialException


have_SDS011 = True
try:
    from sds011 import SDS011
except SerialException:
    have_SDS011 = False
    from mock_sds011 import SDS011


class SDS011Test(TestCase):
    
    @skipUnless( have_SDS011, "Must be on RPi with /dev/ttyUSB0 to run test")
    def test_read(self):
        pm10, pm25 = SDS011(True).read()
        
    
    @skipIf( have_SDS011 , "Test based on Mock SDS011")
    def test_read_mock(self):
        pm10 , pm25 = SDS011(True).read()
        self.assertEqual( pm10 , 10 )
        self.assertEqual( pm25 , 25 )

        
