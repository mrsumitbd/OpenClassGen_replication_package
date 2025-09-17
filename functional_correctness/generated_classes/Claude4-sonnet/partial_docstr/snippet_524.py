class Adder:
    '''A more flexible alternative to Factoryboy sequences. You can create and
        destroy them wherever you want.

    >>> x = Adder(10)
    >>> x(1)
    11
    >>> x(1)
    12
    >>> x.reset(5)
    >>> x(2)
    7
    >>> x(2)
    9
    '''

    def __init__(self, x=0):
        self.current = x

    def __call__(self, value):
        self.current += value
        return self.current

    def reset(self, x):
        self.current = x