import tempfile 
from unittest import TestCase, skipUnless
import os
import os.path
import stat
import requests
import imp
from friskby_client import FriskbyClient
from device_config import DeviceConfig
from friskby_client import FriskbyClient
from context import TestContext


try:
    response = requests.get("https://github.com")
    network = True
except Exception:
    network = False


class FriskbyClientCTest(TestCase):

    def setUp(self):
        self.context = TestContext()

    @skipUnless(network, "Requires network access")
    def test_client(self):
        # The post_key supplied here is not valid for anything, but we pass the "must have post_key test".
        device_config = DeviceConfig.download( "https://friskby.herokuapp.com/sensor/api/device/FriskPI03/" , post_key = "Key")
        client = FriskbyClient(device_config , "SensorID")

    
    def test_import(self):
        client_path = os.path.join( os.path.dirname( __file__ ) , "../bin/fby_client")
        self.assertTrue( os.path.isfile( client_path ) )

        os.environ["FRISKBY_TEST"] = "True"
        client = imp.load_source( "client" , client_path )
        client.network_block( )
        del os.environ["FRISKBY_TEST"]

    @skipUnless(network, "Requires network access")
    def test_post(self):
        client = FriskbyClient( self.context.device_config  , self.context.sensor_id )
        client.post( 0.0 )
        url = self.context.device_config.data["server_url"]
        self.context.device_config.data["server_url"] = "https://friskby.herokuapp.comXXX"
        client.post(1.0)
        client.post(2.0)
        self.assertEqual( len(client.stack) , 2 )
        self.context.device_config.data["server_url"] = url
        client.post(3.0)
        self.assertEqual( len(client.stack) , 0 )
