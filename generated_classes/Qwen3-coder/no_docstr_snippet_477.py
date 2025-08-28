class FctWithCount(object):
    def __init__(self, fct):
        self.fct = fct
        self.count = 0

    def __call__(self, x):
        self.count += 1
        return self.fct(x)