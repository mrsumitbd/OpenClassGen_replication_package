class DisableSignalling:
    '''
    Usage example:
    with DisableSignalling(cls.signal, self.slot):
        # do something
    '''
    def __init__(self, signal, slot):
        self._signal = signal
        self._slot = slot
        self._was_connected = False

    def __enter__(self):
        try:
            # attempt to disconnect; if it wasn't connected, an exception may be raised
            self._signal.disconnect(self._slot)
            self._was_connected = True
        except Exception:
            self._was_connected = False
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._was_connected:
            try:
                self._signal.connect(self._slot)
            except Exception:
                pass
        # allow exceptions to propagate
        return False