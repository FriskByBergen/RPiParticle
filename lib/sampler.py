import time
from ts import TS

class Sampler(object):
    
    def __init__(self, reader, sample_time = None , sleep_time = None, num_sample = None ):
        self.reader = reader
        
        none_count = 0
        if sample_time is None:
            none_count += 1

        if sleep_time is None:
            none_count += 1

        if num_sample is None:
            none_count += 1

        if none_count != 1:
            raise ValueError("Must give exactly two of optional arguments")
            
        if num_sample is None:
            self.sleep_time = sleep_time
            self.num_sample = int(sample_time / sleep_time)
            if sample_time < sleep_time:
                raise ValueError("Invalid time values")
        elif sleep_time is None:
            self.num_sample = num_sample
            self.sleep_time = 1.0 * sample_time / num_sample
        else:
            self.num_sample = num_sample
            self.sleep_time = sleep_time
            

    def collect(self):
        data = []
        for i in range(self.num_sample):
            values = self.reader.read( )
            if len(data) == 0:
                for x in range(len(values)):
                    data.append( TS() )
                
            for index,v in enumerate(values):
                data[index].append( v )
            
            time.sleep( self.sleep_time )

        return data
