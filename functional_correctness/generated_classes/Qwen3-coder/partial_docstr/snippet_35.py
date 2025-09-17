class Mash(object):
    '''
    `Mash` hasing algorithm.

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
        self.state = 0x6a09e667f3bcc908

    def __call__(self, data):
        '''Return mash, updating internal state.'''
        # Convert data to bytes if it's a string
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Process each byte
        for byte in data:
            self.state = (self.state * 0x9e3779b1 + byte) & 0xffffffffffffffff
        
        # Return a float between 0 and 1
        result = (self.state >> 12) / (2**52)
        return result