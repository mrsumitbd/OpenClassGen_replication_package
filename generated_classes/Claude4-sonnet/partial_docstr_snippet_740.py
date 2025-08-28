class Callback(object):
    '''
    Helper class used to listen for an event and then trigger a call
    to a waiting method
    '''

    def __init__(self, method, *args, **kwds):
        self.method = method
        self.args = args
        self.kwds = kwds

    def __call__(self, event):
        return self.method(event, *self.args, **self.kwds)