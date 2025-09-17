class weakattr(object):
    '''Descriptor that transparently wraps its stored value in a weak
    reference.  Reading this attribute will never raise `AttributeError`; if
    the reference is broken or missing, you'll just get `None`.

    To use, create a ``weakattr`` in the class body and assign to it as normal.
    You must provide an attribute name, which is used to store the actual
    weakref in the instance dict.
    '''
    def __init__(self, name):
        self.name = name
        self.storage_name = '_weak_' + name

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        wref = instance.__dict__.get(self.storage_name)
        if wref is None:
            return None
        return wref()

    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = weakref.ref(value)

    def __delete__(self, instance):
        instance.__dict__.pop(self.storage_name, None)