class Mash(object):
    '''
    `Mash` hashing algorithm.

    >>> mash = Mash()
    >>> mash(' ')
    0.8633289230056107
    >>> mash(' ')
    0.15019597788341343
    >>> mash(' ')
    0.9176952994894236
    '''

    def __init__(self):
        '''Initialise state.'''
        self._n = 0xefc8249d

    def __call__(self, data):
        '''Return mash, updating internal state.'''
        for c in str(data):
            self._n += ord(c)
            h = 0.02519603282416938 * self._n
            self._n = int(h)
            h -= self._n
            h *= self._n
            self._n = int(h)
            h -= self._n
            self._n += int(h * 4294967296)
        return (self._n & 0xFFFFFFFF) * 2.3283064365386963e-10