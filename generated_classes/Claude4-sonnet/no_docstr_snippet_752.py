class opt(object):
    def __init__(self, f):
        self.f = f
        self.cache = {}

    def __call__(self, arg):
        if arg not in self.cache:
            self.cache[arg] = self.f(arg)
        return self.cache[arg]