import datetime
import requests
import json



class FriskbyClient(object):
    headers = {'Content-Type': 'application/json'}

    def __init__(self , server_url , sensor_id , post_key):
        self.server_url = server_url
        self.sensor_id = sensor_id
        self.post_key = post_key
        self.stack = []


    def post(self , value):
        timestamp = datetime.datetime.utcnow().isoformat()
        self.stack.insert( (timestamp, value) )

        while True:
            pair = self.stack.pop( )

            data = {"timestamp" : pair[0],
                    "sensorid"  : self.sensor_id,
                    "value"     : pair[1],
                    "key"       : self.post_key }

            respons = requests.post( self.server_url , headers=FriskbyClient.headers, data=json.dumps(data))
            if response.status_code != 201:
                stack.append( pair )
                break
                
            if len(self.stack) == 0:
                break

