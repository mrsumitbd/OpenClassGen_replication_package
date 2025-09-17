class _DomainCheckInterval:
    '''
    Define a valid interval, so that :

    ``domain_check_interval(a,b)(x) == True`` where
    ``x < a`` or ``x > b``.
    '''
    def __init__(self, a, b):
        '''domain_check_interval(a,b)(x) = true where x < a or x > b'''
        if a > b:
            raise ValueError(f"Invalid interval: lower bound {a} is greater than upper bound {b}.")
        self.a = a
        self.b = b

    def __call__(self, x):
        '''Execute the call behavior.'''
        try:
            return (x < self.a) or (x > self.b)
        except TypeError:
            raise TypeError(f"Cannot compare value {x!r} with interval bounds {self.a!r} and {self.b!r}.")