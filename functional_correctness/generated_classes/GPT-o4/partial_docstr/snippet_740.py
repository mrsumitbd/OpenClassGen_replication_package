class Callback(object):
    '''
    Helper class used to listen for an event and then trigger a call
    to a waiting method
    '''

    def __init__(self, method, *args, **kwds):
        self._method = method
        self._args = args
        self._kwds = kwds

    def __call__(self, event):
        return self._method(event, *self._args, **self._kwds)