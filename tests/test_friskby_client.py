import json
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
from requests import ConnectionError, HTTPError

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
        client = FriskbyClient(device_config , "SensorID" , "/tmp")

    
    def test_import(self):
        client_path = os.path.join( os.path.dirname( __file__ ) , "../bin/fby_client")
        self.assertTrue( os.path.isfile( client_path ) )

        os.environ["FRISKBY_TEST"] = "True"
        client = imp.load_source( "client" , client_path )
        client.network_block( )
        del os.environ["FRISKBY_TEST"]

    @skipUnless(network, "Requires network access")
    def test_cache(self):
        fname = "/tmp/%s" % self.context.sensor_id
        d1 = '2016-11-24T22:23:19.271828+00:00'
        d2 = '2016-11-24T22:26:21.182845+00:00'
        with open(fname , "w") as f:
            data = [(d1,100),(d2,200)]
            f.write( json.dumps( data ))
        client = FriskbyClient( self.context.device_config  , self.context.sensor_id , "/tmp" )
        self.assertFalse( os.path.isfile( fname ))
        self.assertTrue( len(client.stack), 2)
        self.assertEqual( client.stack[0][0] , d1 )
        self.assertEqual( client.stack[1][0] , d2 )
        self.assertEqual( client.stack[0][1] , 100 )
        self.assertEqual( client.stack[1][1] , 200 )
        client.post(1.0)
        self.assertTrue( len(client.stack) == 0)

        fname = "/tmp/%s" % self.context.sensor_id
        with open(fname , "w") as f:
            data = [(1,111),(2,222)]
            f.write( json.dumps( data ))

        client = FriskbyClient( self.context.device_config_broken  , self.context.sensor_id , "/tmp" )
        with self.assertRaises(HTTPError):
            client.post(1.0)
        self.assertTrue( len(client.stack), 3)
        self.assertEqual( client.stack[0][0] , 1 )
        self.assertEqual( client.stack[1][0] , 2 )
        self.assertEqual( client.stack[0][1] , 111 )
        self.assertEqual( client.stack[1][1] , 222 )
        self.assertEqual( client.stack[2][1] , 1.0 )



    @skipUnless(network, "Requires network access")
    def test_post(self):
        fname = "/tmp/%s" % self.context.sensor_id
        if os.path.isfile( fname ):
            os.unlink( fname )

        client = FriskbyClient( self.context.device_config  , self.context.sensor_id , "/tmp")
        self.assertEqual( len(client.stack), 0)
        client.post( 0.0 )
        url = self.context.device_config.data["server_url"]
        self.context.device_config.data["server_url"] = "https://friskby.herokuapp.comXXX"
        with self.assertRaises(ConnectionError):
            client.post(1.0)
        with self.assertRaises(ConnectionError):
            client.post(2.0)
        self.assertEqual( len(client.stack) , 2 )
        self.context.device_config.data["server_url"] = url
        client.post(3.0)
        self.assertEqual( len(client.stack) , 0 )
