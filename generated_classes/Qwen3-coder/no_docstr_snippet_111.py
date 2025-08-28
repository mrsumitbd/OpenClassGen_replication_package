class StorageStrategyBase(object):

    def get(self, env_key):
        raise NotImplementedError("Subclasses must implement get method")

    def store(self, token, env_key):
        raise NotImplementedError("Subclasses must implement store method")