class cached_class_property(object):
    '''Simple class property caching descriptor.

    Example:

        >>> class Foo(object):
        >>>     @cached_class_property
        >>>     def bah(cls):
        >>>         print('bah')
        >>>         return 1
        >>>
        >>> Foo.bah
        bah
        1
        >>> Foo.bah
        1
    '''

    def __init__(self, func, name=None):
        self.func = func
        self.name = name or func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, instance, owner=None):
        if owner is None:
            owner = type(instance)
        if self.name in owner.__dict__:
            return owner.__dict__[self.name]
        value = self.func(owner)
        setattr(owner, self.name, value)
        return value