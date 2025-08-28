class ECP_response:
    def __init__(self, content):
        self.content = content
        if isinstance(content, str):
            self.content_bytes = content.encode('utf-8')
        else:
            self.content_bytes = content
        self.headers = [('Content-Type', 'text/html; charset=utf-8')]

    def __call__(self, environ, start_response):
        status = '200 OK'
        start_response(status, self.headers)
        return [self.content_bytes]