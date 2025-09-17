class ConfigModule(object):

    def __init__(self, d, provider=None):
        self._data = d if isinstance(d, dict) else {}
        self._provider = provider
        for key, value in self._data.items():
            if isinstance(value, dict):
                setattr(self, key, ConfigModule(value, provider))
            else:
                setattr(self, key, value)

    @classmethod
    def load(cls, path, provider=None):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(path, 'r') as f:
            if path.endswith('.json'):
                data = json.load(f)
            else:
                # Assume it's a Python file
                content = f.read()
                data = {}
                exec(content, data)
                # Remove built-in variables
                data = {k: v for k, v in data.items() if not k.startswith('__')}
        
        return cls(data, provider)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __contains__(self, key):
        return hasattr(self, key)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                if isinstance(value, ConfigModule):
                    result[key] = value.to_dict()
                else:
                    result[key] = value
        return result