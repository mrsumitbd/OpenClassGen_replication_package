class CollectionMixin:
    def __init__(self):
        pass

    @property
    def Count(self):
        raise NotImplementedError("Count property must be implemented by subclass")

    def Contains(self, item):
        raise NotImplementedError("Contains method must be implemented by subclass")

    def Clear(self):
        raise NotImplementedError("Clear method must be implemented by subclass")

    def CopyTo(self, array, index):
        raise NotImplementedError("CopyTo method must be implemented by subclass")