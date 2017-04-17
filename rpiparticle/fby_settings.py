import json
import os

SETTINGS_PATH = '/usr/local/etc/friskby/friskby-settings.json'


def get_settings_json():
    settings = None
    if (os.path.exists(SETTINGS_PATH)):
        settings = open(SETTINGS_PATH)
    else:
        here = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
        settings = open(os.path.join(here, 'friskby-settings.json'))

    if not settings:
        raise RuntimeError('Could not find any friskby-settings.json.')

    return json.load(settings)


def get_settings():
    return get_settings_json()


def get_setting(setting):
    return get_settings_json().get(setting, '')


def set_setting(key, value):
    settings_json = get_settings_json()
    settings_json[key] = value

    _create_directory_structure()

    with open(SETTINGS_PATH, 'w+') as settings_file:
        json.dump(settings_json, settings_file)


def _create_directory_structure():
    path, _ = os.path.split(SETTINGS_PATH)
    if not os.path.isdir(path):
        os.makedirs(path)  # equivalent to `mkdir -p _path`
