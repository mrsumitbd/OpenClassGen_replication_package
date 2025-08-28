class InstrumentField:
    '''合约'''

    def __init__(self, **kwargs):
        self._attributes = {}
        for key, value in kwargs.items():
            self._attributes[key] = value

    def __setattr__(self, name, value):
        if name == '_attributes':
            object.__setattr__(self, name, value)
        else:
            self._attributes[name] = value

    def __getattr__(self, name):
        try:
            return self._attributes[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __str__(self):
        attrs = ', '.join(f"{k}={v!r}" for k, v in self._attributes.items())
        return f"{type(self).__name__}({attrs})"

    @property
    def __dict__(self):
        return dict(self._attributes)