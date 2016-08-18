import os
import requests
import shutil
import json
import tempfile 
from unittest import TestCase, skipUnless
import os.path
import stat

from service_config import ServiceConfig



class ServiceTest(TestCase):

    def test_load(self):
        with self.assertRaises(IOError):
            sc = ServiceConfig("Does/not/exist")


        template = os.path.abspath( os.path.join( os.path.dirname( __file__ ) , "invalid") )
        with self.assertRaises(ValueError):
            sc = ServiceConfig(template)

        template = os.path.abspath( os.path.join( os.path.dirname( __file__ ) , "../share/friskby") )
        sc = ServiceConfig( template )

        exe = os.path.abspath( os.path.join( os.path.dirname( __file__ ) , "exe") )
        content = sc.render(exe , "FriskBY")
        
