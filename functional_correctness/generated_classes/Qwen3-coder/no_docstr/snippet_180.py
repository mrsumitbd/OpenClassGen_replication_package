class _BlobArgumentWrapper(object):
    def __init__(self, data):
        self._data = data

    @property
    def encoded(self):
        return self._data