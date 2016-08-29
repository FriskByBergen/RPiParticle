import time
import datetime
from ts import TS

class Sampler(object):
    
    def __init__(self, reader, sample_time , sleep_time = 0.10):
        self.reader = reader
        self.sample_time = sample_time
        self.sleep_time = sleep_time


    def collect(self):
        data = []
        start = datetime.datetime.now( )
        while True:
            values = self.reader.read( )
            if len(data) == 0:
                for x in range(len(values)):
                    data.append( TS() )
                
            for index,v in enumerate(values):
                data[index].append( v )
                
            dt = datetime.datetime.now( ) - start
            if dt.total_seconds() >= self.sample_time:
                break
            
            time.sleep( self.sleep_time )


        return data
