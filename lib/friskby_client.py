import os.path
import datetime
import requests
import json
from requests.exceptions import ConnectionError


class FriskbyClient(object):
    headers = {'Content-Type': 'application/json'}

    def __init__(self , device_config , sensor_id, var_path):
        self.device_config = device_config
        self.sensor_id = sensor_id
        self.cache_file = os.path.join( var_path , self.sensor_id)
        self.stack = []
        if os.path.isfile(self.cache_file):
            with open(self.cache_file) as f:
                try:
                    self.stack = json.load( f )
                except:
                    pass
            os.unlink( self.cache_file )

            

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
                with open(self.cache_file , "w") as f:
                    f.write( json.dumps( self.stack ))
                break
                
            if len(self.stack) == 0:
                break

