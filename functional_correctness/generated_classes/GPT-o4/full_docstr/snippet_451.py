class StreamRequestMixin(object):
    """
    `SocketServer.StreamRequestHandler` mixin for adding PROXY protocol
    parsing.
    """

    class ProxyInfo(object):
        __slots__ = (
            'command', 'family',
            'source_address', 'source_port',
            'destination_address', 'destination_port',
            'raw',
        )
        def __init__(self, command, family,
                     source_address, source_port,
                     destination_address, destination_port,
                     raw):
            self.command = command
            self.family = family
            self.source_address = source_address
            self.source_port = source_port
            self.destination_address = destination_address
            self.destination_port = destination_port
            self.raw = raw

    def proxy_authenticate(self, info):
        """
        Authentication hook for parsed proxy information.
        Defaults to ensuring destination (i.e. proxy) is the peer.
        """
        # default: require that the proxy's destination is the real peer
        peer_ip, peer_port = self.client_address[:2]
        return (
            info.destination_address == peer_ip and
            int(info.destination_port) == int(peer_port)
        )

    def proxy_protocol(self, error='raise', default=None,
                       limit=None, authenticate=False):
        """
        Parses, and optionally authenticates, PROXY protocol information
        from request. Note that `self.request` is wrapped by SocketBuffer.
        """
        ppv1_sig = b"PROXY "
        ppv2_sig = b"\r\n\r\n\0\r\nQUIT\n"
        sock = self.request

        def _unread(data):
            # attempt to unread data if wrapper supports it
            if not data:
                return
            u = getattr(sock, 'unread', None)
            if callable(u):
                try:
                    u(data)
                except Exception:
                    pass

        try:
            # peek first 12 bytes to identify
            head = sock.recv(12, socket.MSG_PEEK)
            if not head:
                return default

            # PROXY v1
            if head.startswith(ppv1_sig):
                # read until CRLF, up to limit
                max_bytes = limit or 108
                buf = b''
                while b'\r\n' not in buf:
                    if len(buf) >= max_bytes:
                        raise ValueError("PROXY v1 header too long")
                    chunk = sock.recv(1)
                    if not chunk:
                        raise ValueError("Unexpected EOF reading PROXY v1")
                    buf += chunk
                line, _ = buf.split(b'\r\n', 1)
                parts = line.split()
                if len(parts) != 6:
                    raise ValueError("Invalid PROXY v1 header")
                # parts: [b'PROXY', fam, src, dst, sport, dport]
                fam = parts[1].decode('ascii', 'ignore')
                src = parts[2].decode('ascii', 'ignore')
                dst = parts[3].decode('ascii', 'ignore')
                sport = int(parts[4])
                dport = int(parts[5])
                info = StreamRequestMixin.ProxyInfo(
                    command='PROXY',
                    family=fam,
                    source_address=src,
                    source_port=sport,
                    destination_address=dst,
                    destination_port=dport,
                    raw=buf
                )

            # PROXY v2
            elif head.startswith(ppv2_sig):
                # need 16 bytes to read length
                hdr16 = sock.recv(16, socket.MSG_PEEK)
                if len(hdr16) < 16:
                    raise ValueError("Incomplete PROXY v2 header")
                ver_cmd = hdr16[12]
                fam_proto = hdr16[13]
                length = struct.unpack('!H', hdr16[14:16])[0]
                total = 16 + length
                # peek entire header
                hdr = sock.recv(total, socket.MSG_PEEK)
                if len(hdr) < total:
                    raise ValueError("Incomplete PROXY v2 full header")
                # now consume it
                buf = sock.recv(total)
                cmd = ver_cmd & 0x0F
                if (ver_cmd >> 4) != 0x2 or cmd not in (0x0, 0x1):
                    # invalid version or command
                    info = StreamRequestMixin.ProxyInfo(
                        command='LOCAL',
                        family=None,
                        source_address=None,
                        source_port=None,
                        destination_address=None,
                        destination_port=None,
                        raw=buf
                    )
                else:
                    command = 'PROXY' if cmd == 0x1 else 'LOCAL'
                    af = fam_proto & 0xF0
                    if af == 0x10 and length >= 12:
                        # IPv4
                        src = socket.inet_ntop(socket.AF_INET, buf[16:20])
                        dst = socket.inet_ntop(socket.AF_INET, buf[20:24])
                        sport, dport = struct.unpack('!HH', buf[24:28])
                        famstr = 'TCP4'
                    elif af == 0x20 and length >= 36:
                        # IPv6
                        src = socket.inet_ntop(socket.AF_INET6, buf[16:32])
                        dst = socket.inet_ntop(socket.AF_INET6, buf[32:48])
                        sport, dport = struct.unpack('!HH', buf[48:52])
                        famstr = 'TCP6'
                    else:
                        # unsupported family/proto
                        src = dst = None
                        sport = dport = None
                        famstr = None
                    info = StreamRequestMixin.ProxyInfo(
                        command=command,
                        family=famstr,
                        source_address=src,
                        source_port=sport,
                        destination_address=dst,
                        destination_port=dport,
                        raw=buf
                    )

            # no PROXY header
            else:
                return default

            # at this point, info is built
            if authenticate:
                ok = False
                try:
                    ok = self.proxy_authenticate(info)
                except Exception:
                    ok = False
                if not ok:
                    # undo and return default or raise
                    _unread(info.raw)
                    if error == 'raise':
                        raise RuntimeError("PROXY authentication failed")
                    return default

            return info

        except Exception as e:
            # on error, either raise or unread+return default
            if error == 'raise':
                raise
            # unread any bytes we consumed
            # hard to know exactly, so best effort skip
            # here we did no partial consume on peek,
            # but v1 reads into buf and consumed them
            # so unread buf if present
            try:
                _unread(buf)
            except NameError:
                pass
            return default