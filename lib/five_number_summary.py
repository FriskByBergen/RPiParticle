class FiveNumberSummary():
    """Represents the five number summary that forms the basis of the box-plot.

    Given a list of data points, we extract the min,max,median as well as the q1
    and q3 values (first quartile and third quartile).
    """

    def __init__(self, data):
        tmp = sorted(data)
        l = len(tmp)
        if l == 0:
            raise ValueError('Empty domain')
        summary = [tmp[0], tmp[l//4], tmp[l//2], tmp[3*l//4], tmp[-1]]
        self._summary = tuple(summary)

    def value(self):
        return self.mean()

    def min_value(self):
        return self._summary[0]
    def q1(self):
        return self._summary[1]
    def mean(self):
        return self._summary[2]
    def q3(self):
        return self._summary[3]
    def max_value(self):
        return self._summary[4]
        
    def __str__(self):
        return str(self._summary)

    def __eq__(self, o):
        return o == self._summary

    def __neq(self, o):
        return o != self._summary

    def __getitem__(self, idx):
        return self._summary[idx]

    def __hash__(self):
        return hash(self._summary)

    def __len__(self):
        return len(self._summary) # = 5

    def __min__(self):
        return self.min_value()
    def __max__(self):
        return self.max_value()
