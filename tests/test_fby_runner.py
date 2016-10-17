import os.path
from unittest import TestCase
import imp

client_file = os.path.abspath( os.path.join( os.path.dirname(__file__) , "../bin/fby_client"))
main_module = imp.load_source("fby_client" , client_file)


class FbyRunnerTest(TestCase):

    def test_load(self):
        fby_client = main_module.FbyRunner( ["arg1","arg2"] )
        
