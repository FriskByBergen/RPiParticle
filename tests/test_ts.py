import tempfile 
from unittest import TestCase
import os.path
import stat
from ts import TS

class TSTest(TestCase):

    def test_ts(self):
        ts = TS( )
        self.assertEqual( len(ts) , 0 )
        
        ts.append( 1.0 )
        self.assertEqual( len(ts) , 1 )

        ts.append( 0.0 )
        ts.append( 5.0 )
        self.assertEqual( len(ts) , 3 )
        self.assertEqual( ts.mean() , 2.0 )
