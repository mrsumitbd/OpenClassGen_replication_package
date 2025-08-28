class InjectionContext(object):
    def __init__(self, injector, inherit=False):
        self.injector = injector
        self.inherit = inherit
        self._previous = None

    def _push(self, injector):
        prev = getattr(_thread_local, 'current_injector', None)
        if self.inherit and prev is not None:
            if hasattr(injector, 'set_parent'):
                injector.set_parent(prev)
            elif hasattr(injector, 'parent'):
                try:
                    setattr(injector, 'parent', prev)
                except Exception:
                    pass
        _thread_local.current_injector = injector
        return prev

    def __enter__(self):
        self._previous = self._push(self.injector)
        return self.injector

    def __exit__(self, exc_type, value, traceback):
        if hasattr(_thread_local, 'current_injector'):
            _thread_local.current_injector = self._previous
        self._previous = None