class Numerical(object):
    '''
    Base class for :class:`~exa.core.numerical.Series`,
    :class:`~exa.core.numerical.DataFrame`, and :class:`~exa.numerical.Field`
    objects, providing default trait functionality and clean representations
    when present as part of containers.
    '''

    @property
    def log(self):
        # elementwise natural log
        return np.log(self)

    def slice_naive(self, key):
        '''
        Slice a data object based on its index, either by value (.loc) or
        position (.iloc).

        Args:
            key: Single index value, slice, tuple, or list of indices/positionals

        Returns:
            data: Slice of self
        '''
        # try label-based slicing first
        if hasattr(self, 'loc'):
            try:
                return self.loc[key]
            except (KeyError, IndexError, TypeError):
                pass
        # fallback to positional slicing
        if hasattr(self, 'iloc'):
            try:
                return self.iloc[key]
            except (IndexError, TypeError):
                pass
        # last resort: try plain __getitem__
        try:
            return self[key]
        except Exception as e:
            raise e

    def __repr__(self):
        # clean, minimal container-aware repr
        name = self.__class__.__name__
        content = ''
        if hasattr(self, 'to_string'):
            try:
                content = self.to_string()
            except Exception:
                content = ''
        return f'<{name}{": " + content if content else ""}>'

    def __str__(self):
        return self.__repr__()