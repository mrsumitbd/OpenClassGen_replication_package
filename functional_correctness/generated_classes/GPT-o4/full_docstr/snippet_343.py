class KVStoreServer(object):
    '''The key-value store server.'''

    def __init__(self, kvstore):
        '''Initialize a new KVStoreServer.

        Parameters
        ----------
        kvstore : KVStore
        '''
        self.kvstore = kvstore
        self.controller = self._controller()

    def _controller(self):
        '''Return the server controller.'''
        def server_controller(cmd_id, cmd_body, _):
            action = cmd_body.get('action')
            if action == 'GET':
                key = cmd_body.get('key')
                value = self.kvstore.get(key)
                return {'cmd_id': cmd_id, 'value': value}
            elif action == 'PUT':
                key = cmd_body.get('key')
                value = cmd_body.get('value')
                self.kvstore.put(key, value)
                return {'cmd_id': cmd_id, 'status': 'OK'}
            elif action == 'DELETE':
                key = cmd_body.get('key')
                self.kvstore.delete(key)
                return {'cmd_id': cmd_id, 'status': 'OK'}
            else:
                return {'cmd_id': cmd_id, 'error': 'UNKNOWN_ACTION'}
        return server_controller

    def run(self):
        '''Run the server, whose behavior is like.

        >>> while receive(x):
        ...     if is_command x: controller(x)
        ...     else if is_key_value x: updater(x)
        '''
        while True:
            msg = self.receive()
            if msg is None:
                break
            if self.is_command(msg):
                cmd_id, cmd_body, ctx = msg
                response = self.controller(cmd_id, cmd_body, ctx)
                if response is not None:
                    self.send(response)
            else:
                key, value = msg
                self.kvstore.put(key, value)