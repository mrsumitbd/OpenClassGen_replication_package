class SonarIceClient:
    '''
        Sonar Ice Client. Recives LaserData from Ice interface running Sonar update method in a thread.
    '''

    def __init__(self, ic, prefix, start=False):
        '''
        LaserIceClient Contructor.

        @param ic: Ice Communicator
        @param prefix: prefix name of client in config file
        @param start: indicates if start automatically the client

        @type ic: Ice Communicator
        @type prefix: String
        @type start: Boolean
        '''
        self.ic = ic
        self.prefix = prefix
        self.proxy = None
        self.sonarData = None
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        
        try:
            proxyString = self.ic.getProperties().getProperty(self.prefix + ".Proxy")
            if proxyString:
                self.proxy = self.ic.stringToProxy(proxyString)
        except:
            self.proxy = None
            
        if start:
            self.start()

    def start(self):
        '''
        Starts the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        if not self.running and self.proxy:
            self.running = True
            self.thread = threading.Thread(target=self._update_thread)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        '''
        Stops the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        self.running = False
        if self.thread:
            self.thread.join()

    def getSonarData(self):
        '''
        Returns last LaserData. 

        @return last JdeRobotTypes LaserData saved

        '''
        with self.lock:
            return self.sonarData

    def hasproxy(self):
        '''
        Returns if proxy has ben created or not. 

        @return if proxy has ben created or not (Boolean)

        '''
        return self.proxy is not None

    def _update_thread(self):
        while self.running:
            try:
                if self.proxy:
                    data = self.proxy.getSonarData()
                    with self.lock:
                        self.sonarData = data
            except:
                pass
            time.sleep(0.1)