class _new_initializer(object):
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        instance = self.cls.__new__(self.cls)
        if isinstance(instance, self.cls):
            instance.__init__(*args, **kwargs)
        return instance

    def __str__(self):
        return f"<_new_initializer for {self.cls.__name__}>"

    def __repr__(self):
        return f"_new_initializer({self.cls!r})"