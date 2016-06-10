#!/usr/bin/python3

__author__ = 'njb'

# Enter the correct ID of your Device here:
# DEVICEID = "FriskPI03"
DEVICEID = ....
HEROKU_SENSORIDMP10 = "FriskPI03_PM10"
HEROKU_SENSORIDMP25 = "FriskPI03_PM25" 

#se the reporting interval in minuttes
INTERVAL = 10

import requests
import json
import threading
import time
from time import gmtime, strftime
import datetime

import serial
import schedule

headers = {'Content-Type': 'application/json'}
payload = {'apikey': '571201c719062bc1732021f7'}
headers = {'Content-Type': 'application/json'}

RESTDB_URL = "https://friskbybergen-1d96.restdb.io/rest/posts"
HEROKU_URL = "https://friskby.herokuapp.com/sensor/api/reading/"
HEROKU_KEY = "407f1ef4-2eb2-4299-b977-464e26a094e7"

#choose one of the following depending on how your SDS is connected 
#ser = serial.Serial('/dev/tty.wchusbserial1430', baudrate=9600, stopbits=1, parity="N",  timeout=2)
#ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, stopbits=1, parity="N",  timeout=2)
#ser = serial.Serial('/dev/ttyAMA0', baudrate=9600, stopbits=1, parity="N",  timeout=2)

pm25list = []
pm10list = []

#set the loction of your device
location = [5.3346007,60.3695006]

def job():
    global pm25list
    global pm10list
    print("Posting to RestDB...")
    if len( pm25list) > 0 and len(pm10list) > 0:
        pm25 = round(sum(pm25list) / len(pm25list),2)
        pm10 = round(sum(pm10list) / len(pm10list),2)
        pm25list = []
        pm10list = []
        # print("PM2.5 - ", pm25, " PM10 - ", pm10)
        timestamp = datetime.datetime.utcnow().isoformat()
        data = {'timestamp': timestamp,
                'data': {"PM25": pm25, "PM10":pm10},
                'deviceid': DEVICEID,
                #'location': {'type': 'Point', 'coordinates': location}
                }


        data_heroku_PM10 = {"value"     : pm10,
                            "sensorid"  : "FriskPI03_PM10",
                            "timestamp" : timestamp,
                            "key"       : HEROKU_KEY}
        
        data_heroku_PM25 = {"value"     : pm25,
                            "sensorid"  : "FriskPI03_PM25",
                            "timestamp" : timestamp,
                            "key"       : HEROKU_KEY}

        try:
            requests.post( RESTDB_URL, params=payload, headers=headers, data=json.dumps(data))
            requests.post( HEROKU_URL , headers=headers, data=json.dumps(data_heroku_PM10))
            requests.post( HEROKU_URL , headers=headers, data=json.dumps(data_heroku_PM25))
        except:
            pass

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(INTERVAL).minutes.do(run_threaded, job)

while True:
    schedule.run_pending()
    time.sleep(0.5)
    try:

        s = ser.read(1)
        if ord(s) == int("AA",16):
            s = ser.read(1)
            if ord(s) == int("C0",16):
                s = ser.read(7)
                a = []
                for i in s:
                    a.append(i)
                #print(a)
                pm2hb= s[0]
                pm2lb= s[1]
                pm10hb= s[2]
                pm10lb= s[3]
                cs = s[6]
                # we should verify the checksum... it is the sum of bytes 1-6 truncated...

                try:
                    pm25 = float(pm2hb + pm2lb*256)/10.0
                    pm10 = float(pm10hb + pm10lb*256)/10.0
                    #print("PM2.5 - ", pm25 ," PM10 - ", pm10 )
                    #post2restdb()
                    pm10list.append(pm10)
                    pm25list.append(pm25)
                except:
                    pass
                
        else:
            pass
    except:
        pass
