import os
import requests
import shutil
import json
import tempfile 
from unittest import TestCase, skipUnless
import os.path
import stat

from device_config import DeviceConfig

try:
    response = requests.get("https://github.com")
    network = True
except Exception:
    network = False


class DeviceConfigTest(TestCase):

    def setUp(self):
        fd , self.config_file = tempfile.mkstemp( )
        os.close(fd)

        self.tmpdir = tempfile.mkdtemp( )
        

    def tearDown(self):
        if os.path.isfile( self.config_file ):
            os.unlink( self.config_file )

        if os.path.isdir( self.tmpdir ):
            shutil.rmtree( self.tmpdir )



    def test_create(self):
        with self.assertRaises(IOError):
            config = DeviceConfig("file/not/found")
        
        with open(self.config_file , "w") as f:
            f.write("No - not valid JSON")

        with self.assertRaises(ValueError):
            deviceconfig = DeviceConfig(self.config_file)
        
        conf = {"key" : "value"}
        with open(self.config_file , "w") as f:
            f.write(json.dumps( conf ))

        with self.assertRaises(KeyError):
            config = DeviceConfig(self.config_file)
            
        conf = {"git_repo" : "github" , "git_ref" : "master" , "sensor_list" : ["A","B","C"] , "post_key" : "Key"}
        with open(self.config_file , "w") as f:
            f.write(json.dumps( conf ))
        
        config = DeviceConfig( self.config_file )
        config_file2 = os.path.join( self.tmpdir , "config2")
        config.save( filename = config_file2 )

        config2 = DeviceConfig( config_file2 )
        os.unlink( config_file2 )
        config2.save( )
        self.assertTrue( os.path.isfile( config_file2 ) )

        self.assertTrue( "github" , config2.getRepoURL( ) )


    @skipUnless(network, "Requires network access")
    def test_url_get(self):
        with self.assertRaises(requests.ConnectionError):
            deviceconfig = DeviceConfig.download( "http://does/not/exist" , self.config_file )

        deviceconfig = DeviceConfig.download( "https://friskby.herokuapp.com/sensor/api/device/FriskPI03/" , self.config_file )
        deviceconfig.save( )

