class KVStoreServer(object):
    '''The key-value store server.'''

    def __init__(self, kvstore):
        '''Initialize a new KVStoreServer.

        Parameters
        ----------
        kvstore : KVStore
        '''
        self.kvstore = kvstore

    def _controller(self):
        '''Return the server controller.'''
        def server_controller(cmd_id, cmd_body, _):
            op = cmd_body[0]
            if op == 'GET':
                key = cmd_body[1]
                try:
                    value = self.kvstore.get(key)
                    reply = ('OK', value)
                except KeyError:
                    reply = ('ErrNoKey', None)
            elif op == 'PUT':
                key, value = cmd_body[1], cmd_body[2]
                self.kvstore.put(key, value)
                reply = ('OK', None)
            elif op == 'DELETE':
                key = cmd_body[1]
                try:
                    self.kvstore.delete(key)
                    reply = ('OK', None)
                except KeyError:
                    reply = ('ErrNoKey', None)
            else:
                reply = ('ErrUnknownOp', None)
            return (cmd_id, reply)
        return server_controller

    def run(self):
        '''Run the server, whose behavior is like.

        >>> while receive(x):
        ...     if is_command x: controller(x)
        ...     else if is_key_value x: updater(x)
        '''
        run_server(self._controller(), self.kvstore.updater)