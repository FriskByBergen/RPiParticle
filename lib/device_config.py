import os.path
import json
import requests
import datetime
import tempfile
from urlparse import urlparse

from git_module import GitModule

class DeviceConfig(object):
    config_timeout = 0
    required_keys = ["git_repo" , "git_ref" , "post_key" , "sensor_list" , "post_path" , "config_path" , "server_url" , "device_id"]

    def __init__(self , filename):
        if not os.path.isfile( filename ):
            raise IOError("No such file: %s" % filename)
        
        config = json.load( open(filename) )
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
            new_config = self.download( update_url )
            return new_confi
        except:
            return self


            
    @classmethod
    def download(cls , url):
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
            
        config = DeviceConfig( config_file )
        os.unlink( config_file ) 
        config.filename = None
        
        return config
        

    def postGitVersion(self):
        git_module = GitModule( url = self.getRepoURL() )
        git_module.checkout( self.getGitRef( ) )
        
        data = {"key"     : self.getPostKey(),
                "git_ref" : "%s / %s" % git_module.getHead() }

        response = requests.put("%s/sensor/api/device/%s/" % (self.getServerURL(), self.getDeviceID( )), 
                                data = json.dumps( data ))

