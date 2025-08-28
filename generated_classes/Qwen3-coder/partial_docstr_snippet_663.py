class Numerical(object):
    '''
    Base class for :class:`~exa.core.numerical.Series`,
    :class:`~exa.core.numerical.DataFrame`, and :class:`~exa.numerical.Field`
    objects, providing default trait functionality and clean representations
    when present as part of containers.
    '''

    @property
    def log(self):
        return self._log if hasattr(self, '_log') else None

    def slice_naive(self, key):
        '''
        Slice a data object based on its index, either by value (.loc) or
        position (.iloc).

        Args:
            key: Single index value, slice, tuple, or list of indices/positionals

        Returns:
            data: Slice of self
        '''
        if hasattr(self, 'loc') and hasattr(self, 'iloc'):
            try:
                return self.loc[key]
            except (KeyError, TypeError):
                return self.iloc[key]
        elif hasattr(self, 'iloc'):
            return self.iloc[key]
        elif hasattr(self, 'loc'):
            return self.loc[key]
        else:
            raise NotImplementedError("Slicing not implemented for this numerical object")

    def __repr__(self):
        if hasattr(self, '_repr'):
            return self._repr
        return f"<{self.__class__.__name__} object at {hex(id(self))}>"

    def __str__(self):
        if hasattr(self, '_str'):
            return self._str
        return self.__repr__()