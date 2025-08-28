class toggled_prefetching(object):
    '''Context that toggles prefetching on or off depending on a flag.

    Added in 0.5.0.

    Parameters
    ----------
    enabled : bool
        Whether enabled is activated (``True``) or off (``False``).

    '''
    def __init__(self, enabled):
        self.enabled = bool(enabled)
        self._previous = None

    def __enter__(self):
        global _prefetching_enabled
        self._previous = _prefetching_enabled
        _prefetching_enabled = self.enabled

    def __exit__(self, exception_type, exception_value, exception_traceback):
        global _prefetching_enabled
        _prefetching_enabled = self._previous
        # Do not suppress exceptions
        return False