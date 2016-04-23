__author__ = 'njb'

DEVICEID = "PI1_Gronnlien"
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
payload = {'apikey': 'someapikey'}
url = "https://friskbybergen-1d96.restdb.io/rest/posts"
#ser = serial.Serial('/dev/tty.wchusbserial1430', baudrate=9600, stopbits=1, parity="N",  timeout=2)
ser = serial.Serial('/dev/ttyUSB0', baudrate=9600, stopbits=1, parity="N",  timeout=2)

pm25list = []
pm10list = []
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
        print("PM2.5 - ", pm25, " PM10 - ", pm10)
        data = {'timestamp': datetime.datetime.utcnow().isoformat(),
                'data': {"PM25": pm25, "PM10":pm10},
                'deviceid': DEVICEID,
                #'location': {'type': 'Point', 'coordinates': location}
                }
        try:
            r = requests.post(url, params=payload, headers=headers, data=json.dumps(data))
        except:
            pass

def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()

schedule.every(INTERVAL).minutes.do(run_threaded, job)

while True:
    schedule.run_pending()

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
                    print("PM2.5 - ", pm25 ," PM10 - ", pm10 )
                    #post2restdb()
                    pm10list.append(pm10)
                    pm25list.append(pm25)
                except:
                    pass
                
        else:
            pass
    except:
        pass
