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
        count = len(self._items)
        if index < 0 or index + count > len(array):
            raise IndexError("Index out of range")
        for i, item in enumerate(self._items):
            array[index + i] = item