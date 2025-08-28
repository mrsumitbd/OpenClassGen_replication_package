class InjectionContext(object):
    _stack = []

    def __init__(self, injector, inherit=False):
        self.injector = injector
        self.inherit = inherit
        self.previous_injector = None

    def _push(self, injector):
        if self._stack:
            self._stack.append(injector)
        else:
            self._stack.append(injector)

    def __enter__(self):
        if self._stack and self.inherit:
            self.previous_injector = self._stack[-1]
        else:
            self.previous_injector = None
        
        self._stack.append(self.injector)
        return self

    def __exit__(self, exc_type, value, traceback):
        if self._stack:
            self._stack.pop()