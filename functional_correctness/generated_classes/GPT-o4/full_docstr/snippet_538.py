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

    def __call__(self, *args):
        '''
            Method is being called
        '''
        request = {
            "jsonrpc": "2.0",
            "method": self.method_name,
            "params": args,
            "id": uuid.uuid4().hex
        }
        message = json.dumps(request)
        return self.send_method(self.peer, self.subject, message)