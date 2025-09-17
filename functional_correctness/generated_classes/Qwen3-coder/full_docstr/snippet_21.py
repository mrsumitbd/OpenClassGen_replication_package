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

    def run(self):
        '''Wrapper to start the CherryPy server

        This function throws a PortNotFree exception if any socket error is raised.

        :return: None
        '''
        try:
            self.server = CherryPyWSGIServer(
                (self.host, self.port),
                self.http_interface,
                numthreads=self.thread_pool_size,
                server_name="HTTPDaemon"
            )
            
            if self.use_ssl:
                self.server.ssl_certificate = self.ssl_cert
                self.server.ssl_private_key = self.ssl_key
                if self.ca_cert:
                    self.server.ssl_certificate_chain = self.ca_cert
            
            # Set up logging if specified
            if self.log_file:
                cherrypy.log.access_log.setLevel(cherrypy.log.logging.INFO)
                cherrypy.log.error_log.setLevel(cherrypy.log.logging.INFO)
                cherrypy.log.access_file = self.log_file
                cherrypy.log.error_file = self.log_file
            
            self.server.start()
            
        except socket.error as e:
            raise PortNotFree(f"Port {self.port} is not free: {e}")
        except Exception as e:
            raise e

    def _started_callback(self):
        '''Callback function when Cherrypy Engine is started'''
        pass

    def stop(self):
        '''Wrapper to stop the CherryPy server

        :return: None
        '''
        if self.server:
            self.server.stop()