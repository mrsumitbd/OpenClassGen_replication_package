class Configuration(object):
    """ Defines configuration settings for a search command. """

    def __init__(self, **kwargs):
        self._settings = {}
        for key, val in kwargs.items():
            if not isinstance(key, str) or not key.isidentifier():
                raise ValueError("Invalid configuration key: %r" % key)
            if key.startswith('_'):
                raise ValueError("Configuration key cannot start with underscore: %r" % key)
            self._settings[key] = val

    def __call__(self, cls):
        for key, val in self._settings.items():
            if hasattr(cls, key):
                existing = getattr(cls, key)
                if callable(existing):
                    raise AttributeError(
                        "Cannot override existing method %r on %s" % (key, cls.__name__)
                    )
            setattr(cls, key, val)
        if not hasattr(cls, 'name'):
            name = cls.__name__
            if name.endswith('Command'):
                name = name[:-7]
            cls.name = name.lower()
        return cls