class TS(object):
    """A class for representing time series.

    Remarkably close to just being a list.  But has mean() and median().

    Set accuracy = 3 to get rounding to third decimal.
    """

    def __init__(self, data = None, accuracy=None):
        self.data = []
        self.accuracy = accuracy
        if data:
            for x in data:
                self.append(x)

    def __len__(self):
        return len(self.data)

    def append(self , d):
        if self.accuracy:
            d = round(d, self.accuracy)
        self.data.append( d )

    def __repr__(self):
        return str(self)

    def __str__(self):
        if len(self) < 10:
            return str(self.data)
        tmp = self.data[:4]
        tmp += self.data[-4:]
        fmt = 'TS[{}, {}, {}, {}, ..., {}, {}, {}, {}]'
        return fmt.format(*tmp)

    def mean(self):
        if len(self) == 0:
            raise ValueError('Arithmetic mean of empty time series.')
        return sum(self.data) / float(len(self))

    def median(self):
        if len(self) == 0:
            raise ValueError('Median of empty time series.')
        tmp = sorted(self.data)
        return tmp[len(self)//2]

    def stddev(self):
        ld = len(self.data)
        if ld < 2:
            raise ValueError('Standard deviation of too few values')
        m = self.mean()
        ss = sum((x-m)**2 for x in self.data)
        return (ss/float(ld))**0.5
