class TS(object):
    """A class for representing time series.

    Remarkably close to just being a list.  But has mean() and median().

    """

    def __init__(self, data = None):
        self.data = []
        if data:
            self.data = [x for x in data]

    def __len__(self):
        return len(self.data)

    def append(self , d):
        self.data.append( d )

    def __repr__(self):
        return str(self)

    def __str__(self):
        if len(self) < 10:
            return str(self.data)
        tmp1 = self.data[:4]
        tmp2 = self.data[-4:]
        return 'TS[%f %f %f %f ... %f %f %f %f]' % (tmp1[0], tmp1[1], tmp1[2], tmp1[3],
                                                    tmp2[0], tmp2[1], tmp2[2], tmp2[3])

    def mean(self):
        if len(self) == 0:
            raise ValueError('Arithmetic mean of empty time series.')
        return sum(self.data) / len(self)

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
