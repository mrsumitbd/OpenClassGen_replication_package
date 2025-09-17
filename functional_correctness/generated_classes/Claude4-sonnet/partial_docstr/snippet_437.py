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

    def __get__(self, instance, owner=None):
        if owner is None:
            owner = type(instance)
        
        if hasattr(owner, '_cached_class_properties'):
            cache = owner._cached_class_properties
        else:
            cache = owner._cached_class_properties = {}
        
        if self.name not in cache:
            cache[self.name] = self.func(owner)
        
        return cache[self.name]