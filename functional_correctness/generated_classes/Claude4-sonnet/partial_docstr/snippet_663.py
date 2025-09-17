class Numerical(object):
    '''
    Base class for :class:`~exa.core.numerical.Series`,
    :class:`~exa.core.numerical.DataFrame`, and :class:`~exa.numerical.Field`
    objects, providing default trait functionality and clean representations
    when present as part of containers.
    '''

    @property
    def log(self):
        return logging.getLogger(self.__class__.__name__)

    def slice_naive(self, key):
        '''
        Slice a data object based on its index, either by value (.loc) or
        position (.iloc).

        Args:
            key: Single index value, slice, tuple, or list of indices/positionals

        Returns:
            data: Slice of self
        '''
        if isinstance(key, (int, slice)):
            return self.iloc[key]
        elif isinstance(key, (list, tuple)):
            if all(isinstance(k, int) for k in key):
                return self.iloc[key]
            else:
                return self.loc[key]
        else:
            return self.loc[key]

    def __repr__(self):
        class_name = self.__class__.__name__
        if hasattr(self, 'shape'):
            return f"{class_name}(shape={self.shape})"
        elif hasattr(self, '__len__'):
            return f"{class_name}(length={len(self)})"
        else:
            return f"{class_name}()"

    def __str__(self):
        if hasattr(self, 'to_string'):
            return self.to_string()
        elif hasattr(self, '__array__'):
            return str(self.__array__())
        else:
            return super().__str__()