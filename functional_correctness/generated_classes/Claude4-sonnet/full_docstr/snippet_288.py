class BroadcastMixin(object):
    '''Mix in this class with your Namespace to have a broadcast event method.

    Use it like this:
    class MyNamespace(BaseNamespace, BroadcastMixin):
        def on_chatmsg(self, event):
            self.broadcast_event('chatmsg', event)
    '''

    def broadcast_event(self, event, *args):
        '''
        This is sent to all in the sockets in this particular Namespace,
        including itself.
        '''
        for socket in self.socket.server.sockets.values():
            if hasattr(socket, 'active_ns') and self.ns_name in socket.active_ns:
                socket.active_ns[self.ns_name].emit(event, *args)

    def broadcast_event_not_me(self, event, *args):
        '''
        This is sent to all in the sockets in this particular Namespace,
        except itself.
        '''
        for socket in self.socket.server.sockets.values():
            if (hasattr(socket, 'active_ns') and 
                self.ns_name in socket.active_ns and 
                socket.active_ns[self.ns_name] != self):
                socket.active_ns[self.ns_name].emit(event, *args)