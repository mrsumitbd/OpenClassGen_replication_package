class Stream(object):
    '''A type container for a variable number of types.

    :param args: A sequence of types.

    The :class:`Stream` class is a type container for variable numbers of types.
    Let's say a command returns the content of an internal buffer which can
    contain a variable number of Floats. The corresponding slave command could
    look like this::

        Command('QRY?', 'WRT', Stream(Float))

    A command of alternating floats and integers is therefore writen as::

        Command('QRY?', 'WRT', Stream(Float, Integer))

    '''

    def __init__(self, *types):
        self.types = types

    def simulate(self):
        '''Simulates a stream of types.'''
        import itertools
        return itertools.cycle(self.types)

    def __iter__(self):
        return self.simulate()