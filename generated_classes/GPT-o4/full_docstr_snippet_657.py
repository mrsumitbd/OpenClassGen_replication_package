class Carriage(object):
    '''A base class for carriages.'''

    def __eq__(self, other):
        '''Equivalent to ``self == other``.'''
        if self is other:
            return True
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __hash__(self):
        '''Make this object hashable.'''
        return hash((self.__class__, frozenset(self.__dict__.items())))

    def __repr__(self):
        '''This object as string.'''
        attrs = ', '.join(f"{k}={v!r}" for k, v in sorted(self.__dict__.items()))
        return f"{self.__class__.__name__}({attrs})"