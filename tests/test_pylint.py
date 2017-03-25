from os import listdir
from os.path import isfile, join
import sys
from unittest import TestCase, skipUnless
import subprocess

try:
    subprocess.call(["pylint", "--version"])
    HAVE_PYLINT = True
except OSError:
    msg = '** Warning: Could not find pylint. Static checks skipped'
    sys.stderr.write(msg)
    HAVE_PYLINT = False

class PylintTest(TestCase):

    def _is_python_file(self, path, fname):
        fpath = join(path, fname)
        if not isfile(fpath):
            return False
        if fname[-3:] == '.py':
            return True
        if fname[:4] == 'fby_':
            return True
        if fname == 'run_tests':
            return True
        return False

    def _do_test_files(self, path):
        """pylint -E on all .py files in path"""
        for fname in listdir(path):
            if len(fname) > 2 and self._is_python_file(path, fname):
                fpath = join(path, fname)
                retcode = subprocess.call(["pylint", "-E", fpath])
                self.assertEqual(0, retcode,
                                 msg='linting required for %s' % fpath)

    @skipUnless(HAVE_PYLINT, "Must have pylint executable installed")
    def test_library(self):
        self._do_test_files('bin/')

    @skipUnless(HAVE_PYLINT, "Must have pylint executable installed")
    def test_tests_meta(self):
        self._do_test_files('tests/')
