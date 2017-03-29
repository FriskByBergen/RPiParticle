"""RPiParticle.


This is a small code to sample dust readings from a SDS011 sensor and post the
measurements to a webserver. The executable script will regularly query the
webserver for updates, and if a new version has been configured the script will
invoke git to download a new version and restart itself.

"""

__version__ = '0.7.1'
