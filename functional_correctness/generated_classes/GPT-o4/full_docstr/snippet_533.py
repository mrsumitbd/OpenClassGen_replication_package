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
        self.method_name = method_name
        self.peer = peer
        self.subject = subject
        self.send_method = send_method

    def __call__(self, *args, **kwargs):
        '''
        Method is being called
        '''
        # Generate a unique request ID
        request_id = uuid.uuid4().hex

        # Build params according to JSON-RPC 2.0
        if args and not kwargs:
            params = list(args)
        elif kwargs and not args:
            params = kwargs
        elif args and kwargs:
            params = {
                "args": list(args),
                "kwargs": kwargs
            }
        else:
            params = []

        # Construct the request object
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": self.method_name,
            "params": params
        }

        # Send the request and return the result
        return self.send_method(self.peer, self.subject, request)