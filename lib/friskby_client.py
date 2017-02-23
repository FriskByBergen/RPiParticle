import os.path
import datetime
import requests
import json
from requests.exceptions import ConnectionError


class FriskbyClient(object):
    headers = {'Content-Type': 'application/json'}
        #'Connection'  :  'close'}

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

    def _post_stack(self):
        """Posts the entire stack, or raises an exception.

        If the requests.post does anything but return 201, this function will
        raise an exception (could be HttpError, Timeout, ConnectionRefused,
        Exception).

        If the return code is 201, the stack will be cleared and cache_file
        deleted (unlinked).
        """
        data = {"sensorid"   : self.sensor_id,
                "value_list" : self.stack,
                "key"        : self.device_config.getPostKey( ) }

        respons = requests.post( self.device_config.getPostURL( ) ,
                                 headers=FriskbyClient.headers,
                                 data=json.dumps(data),
                                 timeout=10)
        respons.connection.close()
        if respons.status_code != 201:
            respons.raise_for_status()
            raise Exception('Server did not respond with 201 Created.  Response: %d %s'
                            % (respons.status_code, respons.text))

        self.stack = []
        if os.path.isfile( self.cache_file ):
            os.unlink( self.cache_file )


    def post(self , value):
        timestamp = datetime.datetime.utcnow().isoformat() + "+00:00" # manual TZ

        self.stack.append( (timestamp , value) )

        if len(self.stack) > 0:
            try:
                self._post_stack( )
            except Exception:
                with open(self.cache_file , "w") as f:
                    f.write( json.dumps( self.stack ))
                raise
