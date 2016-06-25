import tempfile 
from unittest import TestCase, skipUnless
import os.path
import stat
import requests
from friskby_client import FriskbyClient
from device_config import DeviceConfig

try:
    response = requests.get("https://github.com")
    network = True
except Exception:
    network = False


class FriskbyClientCTest(TestCase):

    @skipUnless(network, "Requires network access")
    def test_client(self):
        device_config = DeviceConfig.download( "https://friskby.herokuapp.com/sensor/api/device/FriskPI03/")
        client = FriskbyClient(device_config , "SensorID")
