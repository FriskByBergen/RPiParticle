#!/bin/bash

# In addition to the dependencies listed here 'git' is a hard
# dependency. It is assumed that you have already installed git using:
#
#    bash% apt-get install git
#

apt-get install python-pip

pip install -r $(dirname $0)/../requirements.txt

