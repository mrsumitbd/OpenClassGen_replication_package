class Pose3dIceClient:
    '''
        Pose3d Ice Client. Recives Pose3d from Ice interface running Pose3d update method in a thread.
    '''

    def __init__(self, ic, prefix, start=False):
        '''
        Pose3dIceClient Contructor.

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
        self.pose3d = None
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
        
        try:
            proxyString = self.ic.getProperties().getProperty(self.prefix + ".Proxy")
            if proxyString:
                self.proxy = self.ic.stringToProxy(proxyString)
        except:
            self.proxy = None
            
        if start and self.proxy:
            self.start()

    def start(self):
        '''
        Starts the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        if self.proxy and not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._update_pose3d)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        '''
        Stops the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        self.running = False
        if self.thread:
            self.thread.join()

    def getPose3d(self):
        '''
        Returns last Pose3d. 

        @return last JdeRobotTypes Pose3d saved

        '''
        with self.lock:
            return self.pose3d

    def hasproxy(self):
        '''
        Returns if proxy has ben created or not. 

        @return if proxy has ben created or not (Boolean)

        '''
        return self.proxy is not None

    def _update_pose3d(self):
        while self.running:
            try:
                if self.proxy:
                    pose = self.proxy.getPose3DData()
                    with self.lock:
                        self.pose3d = pose
            except:
                pass
            time.sleep(0.05)