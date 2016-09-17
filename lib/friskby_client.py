import datetime
import requests
import json
from requests.exceptions import ConnectionError


class FriskbyClient(object):
    headers = {'Content-Type': 'application/json'}

    def __init__(self , device_config , sensor_id):
        self.device_config = device_config
        self.sensor_id = sensor_id
        self.stack = []


    def post(self , value):
        timestamp = datetime.datetime.utcnow().isoformat()
        self.stack.append( (timestamp, value) )

        while True:
            pair = self.stack.pop( )

            data = {"timestamp" : pair[0],
                    "sensorid"  : self.sensor_id,
                    "value"     : pair[1],
                    "key"       : self.device_config.getPostKey( ) }

            try:
                respons = requests.post( self.device_config.getPostURL( ) , headers=FriskbyClient.headers, data=json.dumps(data))
                if respons.status_code != 201:
                    self.stack.append( pair )
                    break
            except:
                self.stack.append( pair )
                break
                
            if len(self.stack) == 0:
                break

