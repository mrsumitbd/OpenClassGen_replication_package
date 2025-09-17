class HTTPDaemon(object):
    '''HTTP Server class. Mostly based on Cherrypy
    It uses CherryPyWSGIServer and daemon http_interface as Application
    '''

    def __init__(self, host, port, http_interface, use_ssl, ca_cert,
                 ssl_key, ssl_cert, server_dh, thread_pool_size, log_file=None, icon_file=None):
        '''
            Initialize HTTP daemon

            :param host: host address
            :param port: listening port
            :param http_interface:
            :param use_ssl:
            :param ca_cert:
            :param ssl_key:
            :param ssl_cert:
            :param thread_pool_size:
            :param log_file: if set, the log file for Cherrypy log
            :param icon_file: if set, the favicon file to use
        '''
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.ca_cert = ca_cert
        self.ssl_key = ssl_key
        self.ssl_cert = ssl_cert
        self.server_dh = server_dh
        self.thread_pool_size = thread_pool_size
        self.log_file = log_file
        self.icon_file = icon_file
        if icon_file:
            def wrapped_app(environ, start_response):
                if environ.get('PATH_INFO','') == '/favicon.ico':
                    try:
                        with open(self.icon_file, 'rb') as f:
                            data = f.read()
                        ctype = mimetypes.guess_type(self.icon_file)[0] or 'application/octet-stream'
                        headers = [('Content-Type', ctype), ('Content-Length', str(len(data)))]
                        start_response('200 OK', headers)
                        return [data]
                    except IOError:
                        start_response('404 Not Found', [('Content-Type', 'text/plain')])
                        return [b'Not Found']
                return http_interface(environ, start_response)
            self.wsgi_app = wrapped_app
        else:
            self.wsgi_app = http_interface
        self.server = None

    def run(self):
        '''Wrapper to start the CherryPy server

        This function throws a PortNotFree exception if any socket error is raised.

        :return: None
        '''
        def _started_callback():
            '''Callback function when Cherrypy Engine is started'''
            pass

        try:
            self.server = CherryPyWSGIServer((self.host, self.port), self.wsgi_app)
            self.server.thread_pool = self.thread_pool_size
            if self.use_ssl:
                self.server.ssl_certificate = self.ssl_cert
                self.server.ssl_private_key = self.ssl_key
                if self.ca_cert:
                    self.server.ssl_certificate_chain = self.ca_cert
                if hasattr(self.server, 'ssl_server_dh'):
                    self.server.ssl_server_dh = self.server_dh
            if self.log_file:
                try:
                    self.server.log_file = self.log_file
                except Exception:
                    pass
            self.server.start()
        except socket.error as e:
            raise PortNotFree(str(e))

    def stop(self):
        '''Wrapper to stop the CherryPy server

        :return: None
        '''
        if self.server:
            try:
                self.server.stop()
            except:
                pass