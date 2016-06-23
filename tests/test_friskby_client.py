import tempfile 
from unittest import TestCase
import os.path
import stat
from friskby_client import FriskbyClient



class FriskbyClientCTest(TestCase):

    def test_client(self):
        client = FriskbyClient("URL" , "SensorID" , "PostKey")
