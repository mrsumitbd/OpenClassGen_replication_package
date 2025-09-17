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
            '''Server controler.'''
            if cmd_id == 0:  # init
                self.kvstore.init_keys(cmd_body)
            elif cmd_id == 1:  # push
                self.kvstore.push(cmd_body)
            elif cmd_id == 2:  # pull
                self.kvstore.pull(cmd_body)
        
        return server_controller

    def run(self):
        '''Run the server, whose behavior is like.

        >>> while receive(x):
        ...     if is_command x: controller(x)
        ...     else if is_key_value x: updater(x)
        '''
        import mxnet as mx
        controller = self._controller()
        
        def updater(key, recv, local):
            local += recv
        
        server = mx.kv.create('dist_sync')
        server.set_controller(controller)
        server.set_updater(updater)
        server.run()