class LogWrapper(object):
    def __init__(self, context):
        self.context = context
        self.logs = {}

    def __call__(self, key, value):
        self.logs[key] = value
        return self

    def __getattr__(self, name):
        if name in self.logs:
            return self.logs[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")