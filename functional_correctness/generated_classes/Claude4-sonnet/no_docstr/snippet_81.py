class ECP_response:
    def __init__(self, content):
        self.content = content

    def __call__(self, environ, start_response):
        if isinstance(self.content, str):
            content_bytes = self.content.encode('utf-8')
        else:
            content_bytes = self.content
        
        status = '200 OK'
        headers = [
            ('Content-Type', 'application/vnd.paos+xml'),
            ('Content-Length', str(len(content_bytes)))
        ]
        
        start_response(status, headers)
        return [content_bytes]