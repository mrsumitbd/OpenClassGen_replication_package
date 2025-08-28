class _IffHasDelegate(object):
    '''Implements a conditional property using the descriptor protocol.
    Using this class to create a decorator will raise an ``AttributeError``
    if none of the delegates (specified in ``delegate_names``) is an attribute
    of the base object or the first found delegate does not have an attribute
    ``attribute_name``.

    This allows ducktyping of the decorated method based on
    ``delegate.attribute_name``. Here ``delegate`` is the first item in
    ``delegate_names`` for which ``hasattr(object, delegate) is True``.

    See https://docs.python.org/3/howto/descriptor.html for an explanation of
    descriptors.
    '''

    def __init__(self, fn, delegate_names):
        self._fn = fn
        if isinstance(delegate_names, (list, tuple)):
            self.delegate_names = tuple(delegate_names)
        else:
            raise TypeError("delegate_names must be a list or tuple of strings")
        self.__doc__ = fn.__doc__
        self.__name__ = fn.__name__
        # Preserve annotations if present
        if hasattr(fn, '__annotations__'):
            self.__annotations__ = fn.__annotations__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Find the first delegate present on obj
        for name in self.delegate_names:
            if hasattr(obj, name):
                delegate = getattr(obj, name)
                break
        else:
            raise AttributeError(
                f"{type(obj).__name__!r} has no delegate among {self.delegate_names}"
            )
        # Ensure the delegate has the requested attribute
        attr_name = self.__name__
        if not hasattr(delegate, attr_name):
            raise AttributeError(
                f"Delegate {type(delegate).__name__!r} (via '{name}') "
                f"has no attribute {attr_name!r}"
            )
        # Return the attribute bound to the delegate
        return getattr(delegate, attr_name)