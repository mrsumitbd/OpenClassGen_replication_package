class classproperty(object):
    '''A read-only class property.

    Usage is exactly analogous to ``@property`` decorator.
    However, it's only possible to create a getter.
    '''

    def __init__(self, getter):
        self.fget = getter
        self.__doc__ = getter.__doc__
        self.__name__ = getattr(getter, "__name__", None)
        self.__module__ = getattr(getter, "__module__", None)

    def __get__(self, instance, owner):
        if owner is None:
            owner = type(instance)
        return self.fget(owner)

    def __set__(self, instance, value):
        raise AttributeError("can't set class property")

    def __delete__(self, instance):
        raise AttributeError("can't delete class property")