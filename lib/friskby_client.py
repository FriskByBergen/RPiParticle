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


    def post_value(self , timestamp , value):
        try:
            data = {"timestamp" : timestamp,
                    "sensorid"  : self.sensor_id,
                    "value"     : value,
                    "key"       : self.device_config.getPostKey( ) }

            respons = requests.post( self.device_config.getPostURL( ) , 
                                     headers=FriskbyClient.headers, 
                                     data=json.dumps(data))

            if respons.status_code != 201:
                self.stack.append( (timestamp , value) )
        except:
            self.stack.append( (timestamp , value) )


    def post_stack(self):
        data = {"sensorid"   : self.sensor_id,
                "value_list" : self.stack,
                "key"        : self.device_config.getPostKey( ) }

        try:
            respons = requests.post( self.device_config.getPostURL( ) , 
                                     headers=FriskbyClient.headers, 
                                     data=json.dumps(data))
            if respons.status_code != 201:
                raise Exception("Recieved wrong status code")
            self.stack = []
        except:
            pass

        if len(self.stack) == 0:
            if os.path.isfile( self.cache_file ):
                os.unlink( self.cache_file )
        else:
            with open(self.cache_file , "w") as f:
                f.write( json.dumps( self.stack ))
                    

            

    def post(self , value):
        #Manually attached timezone
        timestamp = datetime.datetime.utcnow().isoformat() + "+00:00"
        if len(self.stack) == 0:
            self.post_value( timestamp, value )
        else:
            self.stack.append( (timestamp , value) )

        if len(self.stack) > 0:
            self.post_stack( )
        
