class Handle(object):
    def __init__(self, component):
        self.component = component
        self._iter = None
        self.initialize()

    def initialize(self):
        pass

    def __enter__(self):
        if self._iter is None:
            try:
                self._iter = iter(self.component)
            except TypeError:
                self._iter = None
        if self._iter is not None:
            try:
                return next(self._iter)
            except StopIteration:
                return False
        return False

    def __exit__(self, exc_type, exc_val, exc_tb):
        close = getattr(self.component, "close", None)
        if callable(close):
            try:
                close()
            except Exception:
                pass
        return False

    def slot(self, msg):
        pass