import os.path
import json
import requests
import datetime
import tempfile
from urlparse import urlparse

from git_module import GitModule

class DeviceConfig(object):
    config_timeout = 10 * 60
    required_keys = ["git_repo" , "git_ref" , "post_key" , "sensor_list" , "post_path" , "config_path" , "server_url" , "device_id"]

    def __init__(self , filename , post_key = None):
        if not os.path.isfile( filename ):
            raise IOError("No such file: %s" % filename)
        
        config = json.load( open(filename) )
        if not "post_key" in config:
            if not post_key is None:
                config["post_key"] = post_key
            
        for key in self.required_keys:
            if not key in config:
                raise KeyError("Missing key:%s" % key)

        self.filename = filename
        self.data = config
        self.config_ts = datetime.datetime.now()


    def __eq__(self , other):
        if self.data == other.data:
            return True
        else:
            return False

    def __ne__(self ,other):
        if self == other:
            return False
        else:
            return True


    def save(self , filename = None):
        if filename is None:
            filename  = self.filename
        
        path = os.path.dirname( filename )
        if not os.path.isdir( path ):
            os.makedirs( path )

        with open(filename , "w") as fileH:
            fileH.write( json.dumps( self.data ))


    def getServerURL(self):
        return self.data["server_url"]

    def getConfigPath(self):
        return self.data["config_path"]
        
    def getPostURL(self):
        return "%s/%s" % (self.data["server_url"], self.data["post_path"])

    def getRepoURL(self):
        return self.data["git_repo"]

    def getGitRef(self):
        return self.data["git_ref"]

    def getDeviceID(self):
        return self.data["device_id"]

    def getPostKey(self):
        return self.data["post_key"]


    def downloadNew(self):
        diff = datetime.datetime.now( ) - self.config_ts
        if diff.total_seconds() < self.config_timeout:
            return self

        self.config_ts = datetime.datetime.now( )
        update_url = url = "%s/%s" % (self.getServerURL( ) , self.getConfigPath( ))
        try:
            new_config = self.download( update_url , post_key = self.getPostKey())
            return new_config
        except:
            return self


            
    @classmethod
    def download(cls , url , post_key = None):
        response = requests.get( url )
        if response.status_code != 200:
            raise ValueError("http GET return status:%s" % response.status_code)

        fd , config_file = tempfile.mkstemp( )
        data = json.loads(response.content)
        tmp = urlparse( url )
        config = data["client_config"]
        config["server_url"] = "%s://%s" % (tmp.scheme , tmp.netloc) 
        with open(config_file,"w") as f:
            f.write( json.dumps(config) )
            
        config = DeviceConfig( config_file , post_key = post_key)
        os.unlink( config_file ) 
        config.filename = None
        
        return config
        

    def postGitVersion(self):
        data = {"key"     : self.getPostKey(),
                "git_ref" : self.getGitRef() }
        headers = {"Content-Type": "application/json"}

        response = requests.put("%s/sensor/api/device/%s/" % (self.getServerURL(), self.getDeviceID( )), 
                                data = json.dumps( data ) ,
                                headers = headers )
