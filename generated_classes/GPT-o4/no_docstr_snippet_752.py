class opt(object):
    def __init__(self, f):
        if not callable(f):
            raise TypeError("Expected a callable")
        self.f = f

    def __call__(self, arg):
        return self.f(arg)