#!/usr/bin/env python
from friskby_client import FriskbyClient
from sampler import Sampler
from sds011 import SDS011
from device_config import DeviceConfig
from git_module import GitModule

def restart(config):
    git_module = GitModule( url = config.getRepoURL() )
    git_module.checkout( config.getGitRef( ) )
    git_module.runTests( "tests/run_tests" )
    #git_module.install( )
    #os.fork+++


#choose one of the following depending on how your SDS is connected 
#ser = serial.Serial('/dev/tty.wchusbserial1430', baudrate=9600, stopbits=1, parity="N",  timeout=2)
#ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, stopbits=1, parity="N",  timeout=2)
#ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, stopbits=1, parity="N",  timeout=2)


config = DeviceConfig( config_file )

device_id = config.getDeviceID( )
client_pm10 = FriskbyClient(config , "%s_PM10" % device_id)
client_pm25 = FriskbyClient(config , "%s_PM25" % device_id)
sampler = Sampler( SDS011 , sample_time = SAMPLE_TIME , sleep_time = 0.50 )

while True:
    data = sampler.collect( )
    client_pm10.post( data[0].mean() )
    client_pm25.post( data[1].mean() )

    if config.updateRequired():
        restart(config)
