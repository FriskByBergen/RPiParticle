import os
import requests
import shutil
import sys
import json
import tempfile
from unittest import TestCase, skipUnless
import os.path
import stat
import subprocess

from friskby import DeviceConfig
from context import TestContext


try:
    subprocess.call(["pylint", "--version"])
    have_pylint = True
except OSError:
    sys.stderr.write('** Warning: could not find Python checker "pylint" - static checks skipped')
    have_pylint = False


class PylintTest(TestCase):
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

    @skipUnless(have_pylint,"Must have pylint executable installed")
    def test_binaries(self):
        sys.path.insert(0, os.path.join(self.ROOT, "lib"))
        for prog in ["bin/fby_client", "bin/initrpi"]:
            exit_code = subprocess.check_call(["pylint", "-E", prog])
            self.assertEqual(exit_code, 0)


    @skipUnless(have_pylint,"Must have pylint executable installed")
    def test_library(self):
        module_path = 'python/friskby/'
        for lib in [module_path + 'ts.py',
                    module_path + 'device_config.py',
                    module_path + 'dist.py',
                    module_path + 'git_module.py',
                    module_path + 'sds011.py',
                    module_path + 'wifi_config.py',
                    module_path + 'friskby_dao.py',
                    module_path + 'os_release.py']:

            exit_code = subprocess.check_call(["pylint", "-E", lib])
            self.assertEqual(exit_code, 0)
