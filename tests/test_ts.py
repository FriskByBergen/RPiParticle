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

    def setUp(self):
        self._ts  = TS( [2.71828,3.141592,4.12310] )
        self._tsa = TS( [2.71828,3.141592,4.12310], accuracy=2 )
        self._tsb = TS( [6.1, 5.2, 4.3, 1.2, 2.3, 4.5, 5.6, 1000.123] )
        self._tsc = TS( [6.1, 5.2, 4.3, 1.2, 2.3, 4.5, 5.6, 10.0,12.3] )

    def test_ts_init(self):
        self.assertEqual(3, len(self._ts))
        self.assertEqual(3, len(self._tsa))
        self.assertEqual(8, len(self._tsb))
        self.assertEqual(9, len(self._tsc))
        self.assertEqual(2.72, self._tsa[0])

    def test_math_with_accuracy(self):
        self.assertEqual(3.141592, self._ts.median())
        self.assertEqual(3.14, self._tsa.median())

        self.assertAlmostEqual(3.3276573, self._ts.mean())
        self.assertEqual(3.33, self._tsa.mean())

        self.assertAlmostEqual(0.5884131, self._ts.stddev())
        self.assertEqual(0.59, self._tsa.stddev())

    def test_median(self):
        self.assertEqual(3.141592, self._ts.median())
        self.assertEqual(5.2, self._tsb.median())
        self.assertEqual(5.2, self._tsc.median())
