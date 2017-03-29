import json

SETTINGS_PATH = '/usr/local/etc/friskby/friskby-settings.json'


def get_settings():
    with open(SETTINGS_PATH) as settings:
        return json.load(settings)


def get_setting(setting):
    with open(SETTINGS_PATH) as settings:
        return json.load(settings).get(setting, '')
