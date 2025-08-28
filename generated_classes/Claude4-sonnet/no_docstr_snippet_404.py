class CollectionMixin:
    def __init__(self):
        self._items = []

    @property
    def Count(self):
        return len(self._items)

    def Contains(self, item):
        return item in self._items

    def Clear(self):
        self._items.clear()

    def CopyTo(self, array, index):
        for i, item in enumerate(self._items):
            array[index + i] = item