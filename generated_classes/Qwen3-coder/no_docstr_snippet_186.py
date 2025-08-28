class _new_initializer(object):
    def __init__(self, cls):
        self.cls = cls

    def __call__(self, *args, **kwargs):
        return self.cls(*args, **kwargs)

    def __str__(self):
        return f"_new_initializer({self.cls.__name__})"

    def __repr__(self):
        return f"_new_initializer({self.cls!r})"