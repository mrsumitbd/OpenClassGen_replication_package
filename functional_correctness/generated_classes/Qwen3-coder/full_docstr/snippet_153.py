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
        self.sonarData = jderobot.SonarData()
        self.lock = threading.Lock()
        self.running = False
        self.proxy = None
        self.hasproxy_ = False
        
        # Get property values
        prop = self.ic.getProperties()
        proxy_str = prop.getProperty(prefix + ".Proxy")
        
        if proxy_str:
            try:
                self.proxy = self.ic.stringToProxy(proxy_str)
                self.sonarProxy = jderobot.SonarPrx.checkedCast(self.proxy)
                if self.sonarProxy:
                    self.hasproxy_ = True
            except Exception as e:
                print("Error creating proxy: ", e)
                self.hasproxy_ = False
        
        self.thread = None
        if start and self.hasproxy_:
            self.start()

    def start(self):
        '''
        Starts the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        if not self.running and self.hasproxy_:
            self.running = True
            self.thread = threading.Thread(target=self.updateSonar)
            self.thread.start()

    def stop(self):
        '''
        Stops the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        if self.running:
            self.running = False
            if self.thread and self.thread.is_alive():
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
        return self.hasproxy_

    def updateSonar(self):
        '''
        Internal method to update sonar data in a thread
        '''
        while self.running:
            if self.sonarProxy:
                try:
                    data = self.sonarProxy.getSonarData()
                    with self.lock:
                        self.sonarData = data
                except Exception as e:
                    print("Error getting sonar data: ", e)
            time.sleep(0.05)