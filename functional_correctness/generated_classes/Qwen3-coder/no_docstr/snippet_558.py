class TlmWrapperAttr(object):
    def __init__(self, buffers):
        self._buffers = buffers

    def __getattr__(self, name):
        if name in self._buffers:
            return self._buffers[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")