class _JsonRpcEndpointProxy(object):
    '''
    Proxy to use JSON-RPC over Herald
    '''

    def __init__(self, name, peer, subject, send_method):
        '''
        Sets up the endpoint proxy

        :param name: End point name
        :param peer: UID of the peer to contact
        :param subject: Subject to use for RPC
        :param send_method: Method to use to send a request
        '''
        self._name = name
        self._peer = peer
        self._subject = subject
        self._send_method = send_method

    def __getattr__(self, name):
        '''
        Prefixes the requested attribute name by the endpoint name
        '''
        prefixed_name = '{}.{}'.format(self._name, name)
        return _JsonRpcMethodProxy(prefixed_name, self._peer, self._subject, self._send_method)