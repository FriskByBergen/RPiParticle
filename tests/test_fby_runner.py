import os
from unittest import TestCase
import imp
from random import randint
import sys

client_file = os.path.abspath( os.path.join( os.path.dirname(__file__) , "../bin/fby_client"))
main_module = imp.load_source("fby_client" , client_file)


class FbyRunnerTest(TestCase):

    def setUp(self):
        self._tmp_f = '/tmp/%d' % randint(2**30, 2**32)
        os.mkdir(self._tmp_f)

    def test_load(self):
        fby_client = main_module.FbyRunner(var_path=self._tmp_f)

    def test_sysinfo(self):
        sys_info = main_module.get_sys_info()
        self.assertTrue('sysname'  in sys_info)
        self.assertTrue('requests' in sys_info)
        self.assertTrue('python'   in sys_info)

        import json
        sys_info = main_module.get_sys_info()
        sys_info = json.dumps(sys_info, indent=4, sort_keys=True)
        print(sys_info)

    def test_dao_and_submitter(self):
        fby_client = main_module.FbyRunner(var_path=self._tmp_f)
        dao = fby_client.get_dao()
        self.assertEqual(self._tmp_f + '/friskby.sql', dao.get_path())
        sub = fby_client.get_submitter()
        self.assertEqual(self._tmp_f + '/friskby.sql', sub.get_dao().get_path())
