import os
import requests
import shutil
import json
import tempfile 
from unittest import TestCase, skipUnless
import os.path
import stat

from wifi_config import WifiConfig



class WifiConfigTest(TestCase):

    def test_load(self):
        with self.assertRaises(IOError):
            conf = WifiConfig(config_file = "File/does/not/exist")

        
        config_file = os.path.abspath( os.path.join( os.path.dirname( __file__ ) , "wpa_supplicant.conf") )
        conf = WifiConfig( config_file = config_file )
        
        self.assertFalse( "network_not_defined" in conf.networks() )
        self.assertFalse( "key_not_defined" in conf.settings() )

        self.assertEqual( conf.settings()["update_config"] , "1" )
        self.assertEqual( conf.settings()["country"] , "GB" )
        self.assertEqual( conf.settings()["GROUP"] , "netdev" )
        self.assertTrue( "network1" in conf.networks() )

        conf.addnetwork( "network3", "psk3")
        network3 = conf.networks()["network3"]
        self.assertEqual( network3.ssid , "network3")
        self.assertEqual( network3.psk  , "psk3")

        conf.addnetwork( "network2", "psk22")
        network2 = conf.networks()["network2"]
        self.assertEqual( network2.ssid , "network2")
        self.assertEqual( network2.psk  , "psk22")
        

    def test_write(self):
        config_file = os.path.abspath( os.path.join( os.path.dirname( __file__ ) , "wpa_supplicant.conf") )
        conf = WifiConfig( config_file = config_file )
        fd , name = tempfile.mkstemp()
        conf.save( config_file = name )
        self.assertTrue( os.path.isfile( name ))
        conf2 = WifiConfig( config_file = name )
        
        self.assertEqual( conf2.settings()["update_config"] , "1" )
        self.assertEqual( conf2.settings()["country"] , "GB" )
        self.assertEqual( conf2.settings()["GROUP"] , "netdev" )
        self.assertTrue( "network1" in conf2.networks() )

        network2 = conf2.networks()["network2"]
        self.assertEqual( network2.ssid , "network2")
        self.assertEqual( network2.psk  , "psk2")


    def test_valid_content(self):
        config_file = os.path.abspath( os.path.join( os.path.dirname( __file__ ) , "wpa_supplicant.conf") )
        conf = WifiConfig( config_file = config_file )
        with self.assertRaises( ValueError ):
            conf.addnetwork("", "Secret")

        with self.assertRaises( ValueError ):
            conf.addnetwork("SSID", "")

        with self.assertRaises( ValueError ):
            conf.addnetwork("", "")
        
        self.assertFalse( "ssid" in conf.settings() )
