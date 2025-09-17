class ConfigModule(object):
    def __init__(self, d, provider=None):
        if not isinstance(d, dict):
            raise TypeError("ConfigModule expects a dict")
        self._data = d
        self.provider = provider

    @classmethod
    def load(cls, path, provider=None):
        if not os.path.isfile(path):
            raise FileNotFoundError(f"No such file: {path}")

        _, ext = os.path.splitext(path.lower())
        with open(path, 'r') as f:
            if ext in ('.yaml', '.yml'):
                if yaml is None:
                    raise ImportError("PyYAML is required to load YAML files")
                data = yaml.safe_load(f)
            elif ext == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported file extension: {ext}")

        if not isinstance(data, dict):
            raise ValueError("Configuration file must contain a JSON/YAML object at the top level")

        return cls(data, provider)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __getitem__(self, key):
        return self._data[key]

    def __contains__(self, key):
        return key in self._data

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def as_dict(self):
        return dict(self._data)