import datetime
import requests
import json



class FriskbyClient(object):
    headers = {'Content-Type': 'application/json'}

    def __init__(self , server_url , sensor_id , post_key):
        self.server_url = server_url
        self.sensor_id = sensor_id
        self.post_key = post_key


    def post(self , value):
        timestamp = datetime.datetime.utcnow().isoformat()

        data = {"value"     : value,
                "sensorid"  : self.sensor_id,
                "timestamp" : timestamp,
                "key"       : self.post_key }

        requests.post( self.server_url , headers=FriskbyClient.headers, data=json.dumps(data))
