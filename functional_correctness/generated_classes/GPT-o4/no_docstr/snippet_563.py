class Wrapper:
    def __init__(self, *funcs):
        self.funcs = funcs

    def __call__(self, *args):
        return [f(*args) for f in self.funcs]