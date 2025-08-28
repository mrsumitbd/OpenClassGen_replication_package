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
        self.__name = name
        self.__peer = peer
        self.__subject = subject
        self.__send_method = send_method

    def __getattr__(self, name):
        '''
        Prefixes the requested attribute name by the endpoint name
        '''
        method_name = "{0}.{1}".format(self.__name, name)
        return lambda *args, **kwargs: self.__send_method(
            self.__peer, self.__subject, method_name, args, kwargs
        )