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
        self.irData = None
        self.proxy = None
        self.topic = False
        self._lock = threading.Lock()
        self._running = False
        self._thread = None
        
        # Try to create proxy
        try:
            proxy_str = self.ic.propertyToProxy(self.prefix + ".Proxy")
            if proxy_str:
                self.proxy = self.ic.stringToProxy(proxy_str)
                self.topic = True
        except Exception as e:
            logging.warning("IR Ice Client: Could not create proxy: " + str(e))
            self.topic = False
            
        if start and self.topic:
            self.start()

    def start(self):
        '''
        Starts the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        if not self._running and self.topic:
            self._running = True
            self._thread = threading.Thread(target=self._run)
            self._thread.daemon = True
            self._thread.start()

    def stop(self):
        '''
        Stops the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join()

    def getIRData(self):
        '''
        Returns last LaserData. 

        @return last JdeRobotTypes LaserData saved

        '''
        with self._lock:
            return self.irData

    def hasproxy(self):
        '''
        Returns if proxy has ben created or not. 

        @return if proxy has ben created or not (Boolean)

        '''
        return self.topic

    def _run(self):
        '''
        Main thread loop to receive IR data
        '''
        while self._running:
            try:
                if self.proxy:
                    # Simulate getting IR data - in a real implementation this would call the Ice interface
                    # self.irData = self.proxy.getLaserData()
                    pass
                time.sleep(0.05)  # 20 Hz update rate
            except Exception as e:
                logging.error("IR Ice Client error: " + str(e))
                time.sleep(1)