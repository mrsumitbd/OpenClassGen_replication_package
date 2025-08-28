class Wrapper:
    def __init__(self, *args):
        if len(args) == 1 and callable(args[0]):
            self.func = args[0]
            self.args = ()
            self.kwargs = {}
        else:
            self.func = None
            self.args = args
            self.kwargs = {}

    def __call__(self, *args, **kwargs):
        if self.func is None:
            # Being used as a decorator with arguments
            if len(args) == 1 and callable(args[0]) and not kwargs:
                self.func = args[0]
                return self
            else:
                # Store additional arguments
                self.args = self.args + args
                self.kwargs.update(kwargs)
                return self
        else:
            # Execute the wrapped function
            return self.func(*(self.args + args), **{**self.kwargs, **kwargs})