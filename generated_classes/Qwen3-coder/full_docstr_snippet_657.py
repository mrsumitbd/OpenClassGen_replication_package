class Carriage(object):
    '''A base class for carriages.'''

    def __eq__(self, other):
        '''Equivalent to ``self == other``.'''
        return isinstance(other, self.__class__)

    def __hash__(self):
        '''Make this object hashable.'''
        return hash(self.__class__)

    def __repr__(self):
        '''This object as string.'''
        return f"{self.__class__.__name__}()"