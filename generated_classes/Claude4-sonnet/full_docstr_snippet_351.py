class Interval(object):
    '''
    This class build automatically incrementing interval objects, 
    to be used in requests timeouts
    
    Use like:
    C{interval = Interval()}
    C{t = interval()}
    C{t = interval()}

    @ivar initial:  Initial interval value, in seconds.
    @ivar maxDelay: maximun interval value produced, in seconds.
    @ivar factor:   multiplier for the next interval.
    '''

    def __init__(self, initial=2, maxDelay=1024, factor=2):
        '''Initialize interval object'''
        self.initial = initial
        self.maxDelay = maxDelay
        self.factor = factor
        self.current = initial

    def __call__(self):
        '''Call the interval to produce a new delay time'''
        result = self.current
        self.current = min(self.current * self.factor, self.maxDelay)
        return result