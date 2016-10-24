class TS(object):
    """A class for representing time series.

    Remarkably close to just being a list.  But has mean() and median().

    Set accuracy = 3 to get rounding to third decimal.
    """

    def __init__(self, data = None, accuracy=None):
        self.data = []
        self.accuracy = accuracy
        if data:
            self.data = [x for x in data]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self._round(self.data[idx])

    def append(self , d):
        self.data.append( d )

    def __repr__(self):
        return str(self)

    def _round(self, val):
        if self.accuracy is None:
            return val
        return round(val, self.accuracy)

    def _roundall(self, data):
        if self.accuracy is None:
            return data
        return map(self._round, data)

    def __str__(self):
        if len(self) < 10:
            return str(self._roundall(self.data))

        tmp = self.data[:4]
        tmp += self.data[-4:]
        tmp = self._roundall(tmp)
        fmt = 'TS[{}, {}, {}, {}, ..., {}, {}, {}, {}]'
        return fmt.format(*tmp)

    def mean(self):
        if len(self) == 0:
            raise ValueError('Arithmetic mean of empty time series.')
        m = sum(self.data) / float(len(self))
        return self._round(m)

    def median(self):
        if len(self) == 0:
            raise ValueError('Median of empty time series.')
        tmp = sorted(self.data)
        return self._round(tmp[len(self)//2])

    def stddev(self):
        ld = len(self.data)
        if ld < 2:
            raise ValueError('Standard deviation of too few values')
        m = self.mean()
        ss = sum((x-m)**2 for x in self.data)
        std = (ss/float(ld))**0.5
        return self._round(std)
