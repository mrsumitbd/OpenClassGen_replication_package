class _BlobArgumentWrapper(object):

    def __init__(self, data):
        self.data = data

    @property
    def encoded(self):
        if isinstance(self.data, str):
            return self.data.encode('utf-8')
        elif isinstance(self.data, bytes):
            return self.data
        else:
            return str(self.data).encode('utf-8')