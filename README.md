# RPiParticle ![build status](https://api.travis-ci.org/FriskByBergen/RPiParticle.svg?branch=master "TravisCI Build Status")

## Overview

This is a small code in the _Friskby_ project, the *RPiParticle package* meant
to be run on a RaspberryPi (but can run on any Python-enabled POSIX system) that
deals with the necessary (micro) services for

1. sampling
2. submitting
3. updating
4. controlpanel

More information on the three first can be found at
[python-friskby](https://github.com/FriskByBergen/python-friskby), and the final
can be found at
[python-friskby-controlpanel](https://github.com/FriskByBergen/python-friskby-controlpanel/).

The first three (in `python-friskby`) samples information about the weather,
air, climate or surrounding environment, submits the values to a webserver, and
keeps itself (and us) updated and upgraded.  Security fixes and general
improvements are notified via the updater.

The controlpanel is a webserver running on localhost that displays status
information about our own device.



## Usage

### Installation

You can install `rpiparticle` using pip:

```
sudo pip install rpiparticle
```

This will install the client code as systemd services (the four above mentioned
services for sampling, submitting, etc).

To run RPiParticle, you obtain an _unlocked_ device ID from the friskby project.
If you don't have one, you can either construct it yourself (needs login), or
contact one of the friskby members.

To construct a device,

a. Configure your Device in the Devices table.

b. Configure two sensors attached to your device - these sensor must have the
name of your device, suffix `_PM10` and `_PM25` respectively.

c. Make sure the "Locked" checkbox on your device is *unchecked*.  Observe that
this will automatically be relocked after you have associated the client with
the device id.


After having obtained an unlocked device ID, you can go in to `http://0.0.0.0`.
It will query the user for a device ID and then query the Webserver for a
configuration file (containing post URL and a secret API key) for that device ID
and download and store it to the file system.




### Manual restart

It should not be necessary to manually restart the friskby client, but if things
go wrong for some reason, go to the raspberry pi's website and press `Restart`
or follow these steps:

1. SSH into the device

2. Stop the current client with:
```bash
sudo systemctl restart friskby-sampler
sudo systemctl restart friskby-submitter
sudo systemctl restart friskby
sudo systemctl restart friskby-controlpanel
```
