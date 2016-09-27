# RPiParticle

## Overview

This is a small code to sample dust readings from a SDS011 sensor and
post the measurements to a webserver. The executable script will
regularly query the webserver for updates, and if a new version has
been configured the script will invoke git to download a new version
and restart itself.

## Usage

### Installation

1. Log in to the Raspberry PI and download the code with:

     cd /tmp
     
     git clone https://github.com/FriskByBergen/RPiParticle

   Observe that the code downloaded with this git clone command is
   *not* the code which will eventually run on the client, it is
   therefor important that the git clone commands is performed in a
   temporary location in the filesystem.

2. Run the bin/initrpi script:

     cd RPiParticle/bin
     
     sudo ./initrpi

    The initrpi script consist of three different parts:

    1. It will install all the required dependencies with 'pip
       install'.

    2. It will optionally configure WiFi on the Raspberry PI.

    3. It will query the user for a device ID and then query the
       Webserver for configuration of that device ID, download and
       test the code, and install it.


     





