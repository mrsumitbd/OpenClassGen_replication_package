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
        return info.destination_address == info.peer_address

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
        import pwho
        import pwho.exc as exc
        
        try:
            info = pwho.parse(self.request, limit=limit)
            if info is None:
                if error == 'unread':
                    return default
                else:
                    raise exc.ParseError("No proxy protocol header found")
            
            if authenticate and not self.proxy_authenticate(info):
                raise exc.AuthError("Proxy authentication failed")
                
            return info
            
        except (exc.ReadError, exc.ParseError) as e:
            if error == 'unread':
                # Unread the data back to socket buffer
                if hasattr(self.request, 'unread'):
                    self.request.unread(e.data or b'')
                return default
            else:
                raise
        except exc.AuthError:
            if error == 'unread':
                return default
            else:
                raise