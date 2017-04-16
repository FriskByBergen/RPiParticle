import json
import os
import tempfile
import unittest
from rpiparticle import fby_settings


class SettingsFileExistTestCase(unittest.TestCase):
    # Test scenarios where the settings file exist on the system.

    def setUp(self):
        self.settings_file = tempfile.NamedTemporaryFile()
        fby_settings.SETTINGS_PATH = self.settings_file.name
        json.dump({
            'foo': 'bar'
        }, self.settings_file)

        # Put the cursor at the start of the file.
        self.settings_file.seek(0)

    def tearDown(self):
        self.settings_file.close()

    def test_get_settings(self):
        settings = fby_settings.get_settings()
        self.assertEqual(settings['foo'], 'bar')

    def test_get_setting(self):
        self.assertEqual(fby_settings.get_setting('foo'), 'bar')

    def test_set_setting(self):
        fby_settings.set_setting('foo', 'baz')
        self.assertEqual(fby_settings.get_setting('foo'), 'baz')

    def test_set_new_setting(self):
        fby_settings.set_setting('qux', 'zip')
        self.assertEqual(fby_settings.get_setting('qux'), 'zip')


class SettingsFileDoesNotExistTestCase(unittest.TestCase):
    # Tests scenarios where the settings file does not exist on the system.

    def setUp(self):
        fby_settings.SETTINGS_PATH = '/some/non/existent/path'

    def test_some_settings_works(self):
        self.assertEqual(fby_settings.get_setting('rpi_db'),
                         '/usr/local/var/friskby/friskby.sql')

    def test_saving_some_setting(self):
        """This test is a bit hacky. We create a temporary file, then pass that
        path to fby_settings. When fby_settings creates that file, we read it,
        assert stuff, then close it and remove it.
        """

        # Create and remove a named, temporary file.
        file = tempfile.NamedTemporaryFile()
        fby_settings.SETTINGS_PATH = file.name
        file.close()

        fby_settings.set_setting('rpi_db', '/path/to.sql')

        self.assertEqual(fby_settings.get_setting('rpi_db'),
                         '/path/to.sql')

        # Open the newly created settings file and check things.
        with open(fby_settings.SETTINGS_PATH) as new_settings_file:
            settings = json.load(new_settings_file)
            self.assertEqual(settings['rpi_db'], '/path/to.sql')

        # Clean up.
        os.remove(fby_settings.SETTINGS_PATH)


if __name__ == '__main__':
    unittest.main()
