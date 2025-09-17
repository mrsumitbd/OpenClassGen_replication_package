class FunctionRegistry(object):
    '''
    A registry of functions that can be called all at once.
    '''

    def __init__(self):
        self._functions = []

    def register(self, f, *args, **kwargs):
        '''
        Register a function and arguments to be called later.
        '''
        self._functions.append((f, args, kwargs))

    def run(self):
        '''
        Run all registered functions in reverse order of registration.
        '''
        for f, args, kwargs in reversed(self._functions):
            f(*args, **kwargs)