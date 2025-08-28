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
        self._lock = threading.Lock()
        self._id_counter = 0

    def __getattr__(self, name):
        '''
        Prefixes the requested attribute name by the endpoint name
        '''
        method_name = f"{self._name}.{name}"

        def rpc_method(*args, **kwargs):
            with self._lock:
                self._id_counter += 1
                req_id = self._id_counter

            request = {
                "jsonrpc": "2.0",
                "method": method_name,
                "id": req_id
            }
            if args and kwargs:
                raise ValueError("Cannot mix positional and keyword parameters in JSON-RPC call")
            if args:
                request["params"] = list(args)
            elif kwargs:
                request["params"] = kwargs

            return self._send_method(self._peer, self._subject, request)

        setattr(self, name, rpc_method)
        return rpc_method