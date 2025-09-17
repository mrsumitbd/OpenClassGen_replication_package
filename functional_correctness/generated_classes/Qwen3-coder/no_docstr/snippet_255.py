class ConfigModule(object):
    def __init__(self, d, provider=None):
        self.data = d
        self.provider = provider

    @classmethod
    def load(cls, path, provider=None):
        import json
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(data, provider)