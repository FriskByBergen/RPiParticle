import os
import os.path
import subprocess
import stat

class ServiceConfig(object):
    def __init__(self , template_file, name = "friskby", config_file = "/etc/systemd/system/friskby.service"):
        with open(template_file) as fp:
            self.content = fp.read()

        if self.content.find("%(EXECUTABLE)s") < 0:
            raise ValueError("Missing %(EXECUTABLE)s in template")

        self.config_file = config_file
        self.name = name


    @classmethod
    def systemd(cls):
        return os.path.isdir("/etc/systemd/system")


    def save(self , executable ):
        if os.path.isfile( executable ):
            if os.access( executable , os.X_OK):
                with open(self.config_file , "w") as f:
                    f.write( self.content % {"EXECUTABLE" : os.path.abspath( executable )})
                             
                mode = os.stat( self.config_file ).st_mode
                mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
                os.chmod( self.config_file , mode )
                return
        
        raise OSError("Executable: %s was not usable" % executable)
        

    def enable(self , start = True):
        subprocess.check_call(["systemctl", "daemon-reload"])
        subprocess.check_call(["systemctl", "enable" , self.name])
        if start:
            subprocess.check_call(["systemctl", "start" , self.name])
