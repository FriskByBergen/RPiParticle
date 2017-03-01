from __future__ import absolute_import
import os
import requests
import shutil
import json
import tempfile
from unittest import TestCase, skipUnless
import os.path
import stat

from friskby import ServiceConfig

class ServiceTest(TestCase):

    def test_load(self):
        with self.assertRaises(IOError):
            sc = ServiceConfig("Does/not/exist")


        template = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "invalid"))
        with self.assertRaises(ValueError):
            sc = ServiceConfig(template)

        template = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                "../share/friskby.service"))
        sc = ServiceConfig(template, config_file="/tmp/friskby.service")

        exe = os.path.abspath(os.path.join(os.path.dirname(__file__), "exe"))
        content = sc.save(exe)

    def test_is_systemd(self):
        self.assertEqual(os.path.isdir("/etc/systemd/system"),
                         ServiceConfig.systemd())
