import tempfile 
from unittest import TestCase, skipUnless
import os
import os.path
import stat
import requests
import imp
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

    
    def test_import(self):
        client_path = os.path.join( os.path.dirname( __file__ ) , "../bin/fby_client")
        self.assertTrue( os.path.isfile( client_path ) )

        os.environ["FRISKBY_TEST"] = "True"
        client = imp.load_source( "client" , client_path )
        client.network_block( )
        del os.environ["FRISKBY_TEST"]
        
