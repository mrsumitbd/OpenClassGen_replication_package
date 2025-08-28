class _new_initializer(object):
    def __init__(self, cls):
        self._cls = cls

    def __call__(self, *args, **kwargs):
        return self._cls(*args, **kwargs)

    def __str__(self):
        return f"<new initializer for {self._cls.__name__}>"

    def __repr__(self):
        return f"{self.__class__.__name__}({self._cls!r})"