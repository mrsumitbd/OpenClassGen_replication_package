class opt(object):
    def __init__(self, f):
        self.f = f

    def __call__(self, arg):
        return self.f(arg)