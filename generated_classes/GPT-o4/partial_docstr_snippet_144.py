class Pipe(object):
    '''An object representing a pipe-able callable, optionally with preserved arguments.

    Using this you can construct custom subclasses (define a method named "callable") or use it as a decorator:

            @Pipe
            def s(text):
                    return str(text)

    '''

    def __init__(self, callable, *args, **kw):
        self._func = callable if (callable and hasattr(callable, '__call__')) else None
        self.args = args
        self.kw = kw

    def __repr__(self):
        if self._func:
            name = getattr(self._func, '__name__', repr(self._func))
        else:
            name = self.__class__.__name__
        parts = []
        for a in self.args:
            parts.append(repr(a))
        for k, v in self.kw.items():
            parts.append(f"{k}={v!r}")
        inside = ", ".join(parts)
        return f"{name}({inside})"

    def __ror__(self, other):
        func = self._func if self._func else getattr(self, 'callable')
        return func(other, *self.args, **self.kw)

    def __call__(self, *args, **kw):
        new_args = self.args + args
        new_kw = self.kw.copy()
        new_kw.update(kw)
        return self.__class__(self._func, *new_args, **new_kw)