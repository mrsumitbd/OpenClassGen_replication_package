class StorageStrategyBase(object):
    def __init__(self):
        self._store = {}

    def get(self, env_key):
        return self._store.get(env_key, None)

    def store(self, token, env_key):
        self._store[env_key] = token