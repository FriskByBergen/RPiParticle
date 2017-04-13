# -*- coding: utf-8 -*-
"""
    (c) 2017 FriskbyBergen.

    Licence
    =======
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import fnmatch
import os
import unittest
from pylint import epylint as lint


class CodeTestCase(unittest.TestCase):

    def _get_lintable_files(self, folder):
        matches = []
        for root, _, filenames in os.walk(folder):
            for filename in fnmatch.filter(filenames, '*.py'):
                matches.append(os.path.join(root, filename))
        return matches

    def test_linting(self):
        files = self._get_lintable_files('rpiparticle')
        files = files + self._get_lintable_files('tests')
        for f in files:
            self.assertEqual(lint.lint(f), 0, 'pylint failed')


if __name__ == '__main__':
    unittest.main()
