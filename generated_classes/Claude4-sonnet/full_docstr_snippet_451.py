class StreamRequestMixin(object):
    '''
    `SocketServer.StreamRequestHandler` mixin for adding PROXY protocol
    parsing, e.g.:

    .. code:: python

        import netaddr
        import pwho

        class MyRequestHandler(
                  SocketServer.StreamRequestHandler, pwho.StreamRequestMixin
              ):

            def proxy_authenticate(self, info):
                if not super(MyRequestHandler, self).proxy_authenticate(info):
                    return False
                destination_ip = netaddr.IPAddress(info.destination_address)
                return destination_ip in netaddr.IPNetwork('10/8')

            def handle(self)
                proxy_info = self.proxy_protocol(default='peer', authenticate=True)
                ...

    '''

    def proxy_authenticate(self, info):
        '''
        Authentication hook for parsed proxy information. Defaults to ensuring
        destination (i.e. proxy) is the peer.

        :param info: Parsed ``ProxyInfo`` instance.

        :returns: ``True`` if authenticated, otherwise ``False``.
        '''
        peer_address = self.client_address[0]
        return info.destination_address == peer_address

    def proxy_protocol(self, error='raise', default=None, limit=None, authenticate=False):
        '''
        Parses, and optionally authenticates, proxy protocol information from
        request. Note that ``self.request`` is wrapped by ``SocketBuffer``.

        :param error:
            How read (``exc.ReadError``) and parse (``exc.ParseError``) errors
            are handled. One of:
            - "raise" to propagate.
            - "unread" to suppress exceptions and unread back to socket.
        :param default:
            What to return when no ``ProxyInfo`` was found. Only meaningful
            with error "unread".
        :param limit:
            Maximum number of bytes to read when probing request for
            ``ProxyInfo``.

        :returns: Parsed ``ProxyInfo`` instance or **default** if none found.
        '''
        if not hasattr(self, '_socket_buffer'):
            self._socket_buffer = SocketBuffer(self.request)
            self.request = self._socket_buffer
        
        if limit is None:
            limit = 1024
        
        try:
            data = self.request.read(limit)
            if not data:
                if error == 'raise':
                    raise exc.ReadError("No data received")
                elif error == 'unread':
                    return default
            
            info = parse_proxy_protocol(data)
            
            if info is None:
                if error == 'raise':
                    raise exc.ParseError("No proxy protocol found")
                elif error == 'unread':
                    self.request.unread(data)
                    return default
            
            if authenticate and not self.proxy_authenticate(info):
                if error == 'raise':
                    raise exc.ParseError("Proxy authentication failed")
                elif error == 'unread':
                    self.request.unread(data)
                    return default
            
            remaining_data = data[info.consumed_bytes:]
            if remaining_data:
                self.request.unread(remaining_data)
            
            return info
            
        except (exc.ReadError, exc.ParseError) as e:
            if error == 'raise':
                raise
            elif error == 'unread':
                if 'data' in locals():
                    self.request.unread(data)
                return default