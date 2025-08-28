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
        if hasattr(self, 'socket') and hasattr(self.socket, 'server'):
            self.socket.server.broadcast(event, *args, namespace=self.__class__.__name__)
        elif hasattr(self, 'emit'):
            # Fallback to emit to all clients in this namespace
            self.emit(event, *args, broadcast=True)

    def broadcast_event_not_me(self, event, *args):
        '''
        This is sent to all in the sockets in this particular Namespace,
        except itself.
        '''
        if hasattr(self, 'socket') and hasattr(self.socket, 'server'):
            self.socket.server.broadcast(event, *args, namespace=self.__class__.__name__, skip_sid=self.socket.sid)
        elif hasattr(self, 'emit'):
            # Fallback to emit to all clients except sender
            self.emit(event, *args, broadcast=True, include_self=False)