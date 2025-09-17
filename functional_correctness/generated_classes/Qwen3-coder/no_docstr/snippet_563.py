class Wrapper:
    def __init__(self, *args):
        self.args = args

    def __call__(self, *args):
        return self.args + args