class FunctionRegistry(object):
    '''
    A registry of functions that can be called all at once.
    '''

    def __init__(self):
        self._registry = []

    def register(self, f, *args, **kwargs):
        '''
        Register a function and arguments to be called later.
        '''
        if not callable(f):
            raise TypeError("First argument must be callable")
        self._registry.append((f, args, kwargs))

    def run(self):
        '''
        Run all registered functions in reverse order of registration.
        '''
        for func, args, kwargs in reversed(self._registry):
            func(*args, **kwargs)