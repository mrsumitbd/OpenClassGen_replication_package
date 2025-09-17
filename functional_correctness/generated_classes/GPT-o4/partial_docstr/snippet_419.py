class IPyAutocall(object):
    ''' Instances of this class are always autocalled
    
    This happens regardless of 'autocall' variable state. Use this to
    develop macro-like mechanisms.
    '''
    def __init__(self, ip=None):
        self._ip = None
        if ip is not None:
            self.set_ip(ip)

    def set_ip(self, ip):
        ''' Will be used to set _ip point to current ipython instance b/f call
        
        Override this method if you don't want this to happen.
        
        '''
        self._ip = ip

    def __call__(self, arg_s=None, *args, **kwargs):
        return self.call(arg_s, *args, **kwargs)

    def call(self, arg_s, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the call() method")