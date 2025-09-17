class TlmWrapperAttr(object):
    def __init__(self, buffers):
        # buffers: an iterable of objects or dict-like
        self._buffers = list(buffers)

    def __getattr__(self, name):
        for buf in self._buffers:
            # try object attribute
            try:
                return getattr(buf, name)
            except AttributeError:
                pass
            # try dict-like access
            try:
                return buf[name]
            except (TypeError, KeyError):
                pass
        raise AttributeError(f"{self.__class__.__name__!r} object has no attribute {name!r}")