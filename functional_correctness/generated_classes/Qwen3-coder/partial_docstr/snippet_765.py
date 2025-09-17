class classproperty(object):
    '''A read-only class property.

    Usage is exactly analogous to ``@property`` decorator.
    However, it's only possible to create a getter.
    '''

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        if owner is None:
            return self
        return self.getter(owner)