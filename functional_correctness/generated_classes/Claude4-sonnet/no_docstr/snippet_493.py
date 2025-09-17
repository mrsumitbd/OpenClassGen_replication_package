class LogWrapper(object):
    def __init__(self, context):
        self.context = context
        self.data = {}

    def __call__(self, key, value):
        self.data[key] = value
        return self

    def __getattr__(self, name):
        if name in self.data:
            return self.data[name]
        return getattr(self.context, name)