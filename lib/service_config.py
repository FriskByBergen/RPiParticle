import os
import os.path

class ServiceConfig(object):
    def __init__(self , template_file):
        with open(template_file) as fp:
            self.content = fp.read()

        if self.content.find("%(NAME)s") < 0:
            raise ValueError("Missing %(NAME)s in template")

        if self.content.find("%(EXECUTABLE)s") < 0:
            raise ValueError("Missing %(EXECUTABLE)s in template")


    def render(self , executable , name):
        if os.path.isfile( executable ):
            if os.access( executable , os.X_OK):
                return self.content % {"EXECUTABLE" : os.path.abspath( executable ), "NAME" : name}
        
        raise OSError("Executable: %s was not usable" % executable)
        
