class ECP_response:
    def __init__(self, content):
        if isinstance(content, (list, tuple)):
            parts = []
            for part in content:
                if isinstance(part, str):
                    part = part.encode('utf-8')
                parts.append(part)
            self._body = b''.join(parts)
        elif isinstance(content, str):
            self._body = content.encode('utf-8')
        elif isinstance(content, bytes):
            self._body = content
        else:
            raise TypeError("content must be bytes, str, or list/tuple of them")

    def __call__(self, environ, start_response):
        status = '200 OK'
        headers = [
            ('Content-Type', 'application/xml; charset=utf-8'),
            ('Content-Length', str(len(self._body)))
        ]
        start_response(status, headers)
        return [self._body]