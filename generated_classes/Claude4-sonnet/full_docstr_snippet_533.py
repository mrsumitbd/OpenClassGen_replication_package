class _JsonRpcMethod(object):
    '''
    Represents a method in a call proxy
    '''

    def __init__(self, method_name, peer, subject, send_method):
        '''
        Sets up the method

        :param method_name: Full method name
        :param peer: UID of the peer to contact
        :param subject: Subject to use for RPC
        :param send_method: Method to use to send a request
        '''
        self._method_name = method_name
        self._peer = peer
        self._subject = subject
        self._send_method = send_method

    def __call__(self, *args, **kwargs):
        '''
        Method is being called
        '''
        return self._send_method(self._peer, self._subject, self._method_name, *args, **kwargs)