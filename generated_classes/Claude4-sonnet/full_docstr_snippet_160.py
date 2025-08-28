class IRIceClient:
    '''
        IR Ice Client. Recives LaserData from Ice interface running IR update method in a thread.
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
        self.ir_data = None
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        
        try:
            proxystr = self.ic.getProperties().getProperty(self.prefix + ".Proxy")
            if proxystr:
                self.proxy = self.ic.stringToProxy(proxystr)
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
            self.thread = threading.Thread(target=self._update_loop)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        '''
        Stops the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        self.running = False
        if self.thread:
            self.thread.join()

    def getIRData(self):
        '''
        Returns last LaserData. 

        @return last JdeRobotTypes LaserData saved

        '''
        with self.lock:
            return self.ir_data

    def hasproxy(self):
        '''
        Returns if proxy has ben created or not. 

        @return if proxy has ben created or not (Boolean)

        '''
        return self.proxy is not None

    def _update_loop(self):
        '''
        Internal method that runs in a separate thread to continuously update IR data
        '''
        while self.running:
            try:
                if self.proxy:
                    data = self.proxy.getLaserData()
                    with self.lock:
                        self.ir_data = data
            except:
                pass
            time.sleep(0.1)