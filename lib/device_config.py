import os.path
import json
import requests
import tempfile

class DeviceConfig(object):
    required_keys = ["git_repo" , "git_ref" , "post_key" , "sensor_list"]

    def __init__(self , filename):
        if not os.path.isfile( filename ):
            raise IOError("No such file: %s" % filename)
        
        config = json.load( open(filename) )
        for key in self.required_keys:
            if not key in config:
                raise KeyError("Missing key:%s" % key)

        self.filename = filename
        self.data = config


    def save(self , filename = None):
        if filename:
            fileH = open(filename , "w")
        else:
            fileH = open(self.filename , "w")

        fileH.write( json.dumps( self.data ))


    def getRepoURL(self):
        return self.data["git_repo"]

    def getGitRef(self):
        return self.data["git_ref"]


    @classmethod
    def download(cls , url , target_file):
        response = requests.get( url )
        if response.status_code != 200:
            raise ValueError("http GET return status:%s" % response.status_code)

        fd , config_file = tempfile.mkstemp( )
        data = json.loads(response.content)
        with open(config_file,"w") as f:
            f.write( json.dumps(data["client_config"] ))
            
        config = DeviceConfig( config_file )
        os.unlink( config_file ) 
        config.filename = target_file
        
        return config
        
