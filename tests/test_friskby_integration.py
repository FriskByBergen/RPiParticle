from unittest import TestCase
from random import randint

from friskby import TS

class FriskbyIntegration(TestCase):

    def test_ts(self):
        t = TS()
        t.append(4)
        t.append(6)
        self.assertEqual(5.0, t.mean())
