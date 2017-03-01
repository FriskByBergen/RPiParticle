from __future__ import (absolute_import, print_function)
import os
import json
from unittest import TestCase
from random import randint

from friskby import FriskbyRunner


class FriskbyRunnerTest(TestCase):

    def setUp(self):
        self._tmp_f = '/tmp/%d' % randint(2**30, 2**32)
        os.mkdir(self._tmp_f)

    def test_load(self):
        _ = FriskbyRunner(var_path=self._tmp_f)

    def test_sysinfo(self):
        sys_info = FriskbyRunner.get_sys_info()
        self.assertTrue('sysname'  in sys_info)
        self.assertTrue('requests' in sys_info)
        self.assertTrue('python'   in sys_info)

        sys_info = FriskbyRunner.get_sys_info()
        sys_info = json.dumps(sys_info, indent=4, sort_keys=True)
        print(sys_info)
