"""RPiParticle.


This is a small code to sample dust readings from a SDS011 sensor and post the
measurements to a webserver. The executable script will regularly query the
webserver for updates, and if a new version has been configured the script will
invoke git to download a new version and restart itself.

"""
__version__ = '0.9.3'

from .fby_settings import get_setting, get_settings

__all__ = ['get_setting', 'get_settings']
