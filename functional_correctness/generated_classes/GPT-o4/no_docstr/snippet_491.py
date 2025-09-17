class Buffer(object):

    def __init__(self, keys, n=None):
        self._keys = set(keys)
        self._n = n
        self._buffer = deque()

    def __contains__(self, item):
        return item in self._keys

    def is_readable(self):
        return bool(self._buffer)

    def is_writable(self, key):
        if key not in self._keys:
            return False
        if self._n is None:
            return True
        return len(self._buffer) < self._n

    def read(self):
        if not self.is_readable():
            raise BufferError("Buffer is empty")
        return self._buffer.popleft()

    def write(self, key, values):
        if key not in self._keys:
            raise KeyError(f"Invalid key: {key}")
        if not self.is_writable(key):
            raise BufferError("Buffer is full")
        self._buffer.append((key, values))