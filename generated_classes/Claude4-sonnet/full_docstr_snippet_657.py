class Carriage(object):
    '''A base class for carriages.'''

    def __eq__(self, other):
        '''Equivalent to ``self == other``.'''
        if not isinstance(other, Carriage):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self):
        '''Make this object hashable.'''
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self):
        '''This object as string.'''
        return f"{self.__class__.__name__}()"