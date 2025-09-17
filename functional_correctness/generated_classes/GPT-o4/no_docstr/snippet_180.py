class _BlobArgumentWrapper(object):
    def __init__(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        elif not isinstance(data, (bytes, bytearray)):
            raise TypeError('data must be bytes or str')
        self._data = data

    @property
    def encoded(self):
        return base64.b64encode(self._data).decode('ascii')