#!/usr/bin/env python
from friskby_client import FriskbyClient
from sampler import Sampler
from sds011 import SDS011

#choose one of the following depending on how your SDS is connected 
#ser = serial.Serial('/dev/tty.wchusbserial1430', baudrate=9600, stopbits=1, parity="N",  timeout=2)
#ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, stopbits=1, parity="N",  timeout=2)
#ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, stopbits=1, parity="N",  timeout=2)


client_pm10 = FriskbyClient(HEROKU_URL , "%s_PM10" % DEVICEID , HEROKU_KEY)
client_pm25 = FriskbyClient(HEROKU_URL , "%s_PM25" % DEVICEID , HEROKU_KEY)
sampler = Sampler( SDS011 , sample_time = SAMPLE_TIME , sleep_time = 0.50 )
while True:
    data = sampler.collect( )
    
    client_pm10.post( data[0].mean() )
    client_pm25.post( data[1].mean() )
