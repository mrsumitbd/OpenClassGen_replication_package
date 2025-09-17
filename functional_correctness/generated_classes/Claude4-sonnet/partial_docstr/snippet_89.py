class weakattr(object):
    '''Descriptor that transparently wraps its stored value in a weak
    reference.  Reading this attribute will never raise `AttributeError`; if
    the reference is broken or missing, you'll just get `None`.

    To use, create a ``weakattr`` in the class body and assign to it as normal.
    You must provide an attribute name, which is used to store the actual
    weakref in the instance dict.

    .. code-block:: python

        class Foo(object):
            bar = weakattr('bar')

            def __init__(self, bar):
                self.bar = bar

    >>> class Dummy(object): pass
    >>> obj = Dummy()
    >>> foo = Foo(obj)
    >>> assert foo.bar is obj
    >>> print(foo.bar)
    <object object at ...>
    >>> del obj
    >>> print(foo.bar)
    None

    Of course, if you try to assign a value that can't be weak referenced,
    you'll get a ``TypeError``.  So don't do that.  In particular, a lot of
    built-in types can't be weakref'd!

    Note that due to the ``__dict__`` twiddling, this descriptor will never
    trigger ``__getattr__``, ``__setattr__``, or ``__delattr__``.
    '''

    def __init__(self, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        weakref_obj = instance.__dict__.get(self.name)
        if weakref_obj is None:
            return None
        return weakref_obj()

    def __set__(self, instance, value):
        if value is None:
            instance.__dict__[self.name] = None
        else:
            instance.__dict__[self.name] = weakref.ref(value)

    def __delete__(self, instance):
        instance.__dict__.pop(self.name, None)