class _DomainCheckInterval:
    '''
    Define a valid interval, so that :

    ``domain_check_interval(a,b)(x) == True`` where
    ``x < a`` or ``x > b``.

    '''

    def __init__(self, a, b):
        '''domain_check_interval(a,b)(x) = true where x < a or y > b'''
        self.a = a
        self.b = b

    def __call__(self, x):
        '''Execute the call behavior.'''
        return x < self.a or x > self.b