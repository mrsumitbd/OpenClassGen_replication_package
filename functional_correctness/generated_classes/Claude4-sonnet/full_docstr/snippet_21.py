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
        self.http_interface = http_interface
        self.use_ssl = use_ssl
        self.ca_cert = ca_cert
        self.ssl_key = ssl_key
        self.ssl_cert = ssl_cert
        self.server_dh = server_dh
        self.thread_pool_size = thread_pool_size
        self.log_file = log_file
        self.icon_file = icon_file
        self.server = None
        
        # Configure CherryPy
        cherrypy.config.update({
            'server.socket_host': self.host,
            'server.socket_port': self.port,
            'server.thread_pool': self.thread_pool_size,
            'engine.autoreload.on': False,
            'log.screen': False
        })
        
        if self.log_file:
            cherrypy.config.update({
                'log.access_file': self.log_file,
                'log.error_file': self.log_file
            })
        
        if self.use_ssl:
            cherrypy.config.update({
                'server.ssl_module': 'builtin',
                'server.ssl_certificate': self.ssl_cert,
                'server.ssl_private_key': self.ssl_key
            })
            if self.ca_cert:
                cherrypy.config.update({
                    'server.ssl_certificate_chain': self.ca_cert
                })

    def run(self):
        '''Wrapper to start the CherryPy server

        This function throws a PortNotFree exception if any socket error is raised.

        :return: None
        '''
        try:
            cherrypy.engine.subscribe('start', self._started_callback)
            
            # Mount the application
            cherrypy.tree.mount(self.http_interface, '/')
            
            # Start the engine
            cherrypy.engine.start()
            cherrypy.engine.wait(cherrypy.engine.states.STARTED)
            
        except socket.error as e:
            raise PortNotFree(f"Port {self.port} is not available: {e}")
        except Exception as e:
            raise PortNotFree(f"Failed to start server: {e}")

    def _started_callback(self):
        '''Callback function when Cherrypy Engine is started'''
        protocol = "https" if self.use_ssl else "http"
        print(f"HTTP daemon started on {protocol}://{self.host}:{self.port}")

    def stop(self):
        '''Wrapper to stop the CherryPy server

        :return: None
        '''
        if cherrypy.engine.state == cherrypy.engine.states.STARTED:
            cherrypy.engine.exit()