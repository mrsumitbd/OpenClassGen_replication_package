class KVStoreServer(object):
    '''The key-value store server.'''

    def __init__(self, kvstore):
        '''Initialize a new KVStoreServer.

        Parameters
        ----------
        kvstore : KVStore
        '''
        self.kvstore = kvstore
        self.running = False

    def _controller(self):
        '''Return the server controller.'''
        def server_controller(cmd_id, cmd_body, _):
            '''Server controller.'''
            # Handle different command types based on cmd_id
            if cmd_id == 'GET':
                key = cmd_body.get('key')
                return self.kvstore.get(key)
            elif cmd_id == 'PUT':
                key = cmd_body.get('key')
                value = cmd_body.get('value')
                self.kvstore.put(key, value)
                return 'OK'
            elif cmd_id == 'DELETE':
                key = cmd_body.get('key')
                self.kvstore.delete(key)
                return 'OK'
            else:
                return 'UNKNOWN_COMMAND'
        return server_controller

    def run(self):
        '''Run the server, whose behavior is like.


        >>> while receive(x):
        ...     if is_command x: controller(x)
        ...     else if is_key_value x: updater(x)
        '''
        self.running = True
        controller = self._controller()
        
        while self.running:
            try:
                x = self._receive()  # Assuming this method exists to receive data
                if self._is_command(x):
                    response = controller(x['cmd_id'], x['cmd_body'], None)
                    self._send_response(response)  # Assuming this method exists to send response
                elif self._is_key_value(x):
                    self._updater(x)  # Assuming this method exists to handle key-value updates
            except Exception as e:
                # Handle exceptions and potentially break the loop if needed
                if not self.running:
                    break

    def _receive(self):
        '''Placeholder for receiving data - should be implemented based on actual communication method.'''
        # This would typically block and wait for incoming data
        raise NotImplementedError("Receive method needs to be implemented")

    def _is_command(self, x):
        '''Check if received data is a command.'''
        return isinstance(x, dict) and 'cmd_id' in x and 'cmd_body' in x

    def _is_key_value(self, x):
        '''Check if received data is a key-value pair.'''
        return isinstance(x, dict) and 'key' in x and 'value' in x

    def _updater(self, x):
        '''Handle key-value updates.'''
        key = x.get('key')
        value = x.get('value')
        self.kvstore.put(key, value)

    def _send_response(self, response):
        '''Placeholder for sending response - should be implemented based on actual communication method.'''
        # This would send the response back to the client
        pass

    def stop(self):
        '''Stop the server.'''
        self.running = False