

class TS(object):

    def __init__(self):
        self.data = []


    def __len__(self):
        return len(self.data)

    def append(self , d):
        self.data.append( d )


    def mean(self):
        return sum(self.data) / len(self)
