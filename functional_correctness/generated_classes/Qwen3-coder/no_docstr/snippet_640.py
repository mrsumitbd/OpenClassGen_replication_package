class InjectionContext(object):
    def __init__(self, injector, inherit=False):
        self.injector = injector
        self.inherit = inherit
        self.previous_context = None

    def _push(self, injector):
        self.previous_context = self.injector.get_current_context()
        self.injector.set_current_context(self)

    def __enter__(self):
        if self.inherit and self.previous_context is not None:
            self._push(self.injector)
        else:
            self._push(self.injector)
        return self

    def __exit__(self, exc_type, value, traceback):
        if self.previous_context is not None:
            self.injector.set_current_context(self.previous_context)
        else:
            self.injector.set_current_context(None)