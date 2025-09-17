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
        mgr = getattr(self, 'manager', None)
        if mgr is None:
            return
        ns_map = getattr(mgr, 'namespaces', {}).get(self.ns_name, {})
        for ns in ns_map.values():
            ns.emit(event, *args)

    def broadcast_event_not_me(self, event, *args):
        '''
        This is sent to all in the sockets in this particular Namespace,
        except itself.
        '''
        mgr = getattr(self, 'manager', None)
        if mgr is None:
            return
        ns_map = getattr(mgr, 'namespaces', {}).get(self.ns_name, {})
        for ns in ns_map.values():
            if ns is not self:
                ns.emit(event, *args)