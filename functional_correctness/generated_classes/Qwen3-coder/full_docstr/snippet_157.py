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
        self.pose3d = None
        self.proxy = None
        self.topic = False
        self.started = False
        self.running = False
        self.thread = None
        
        # Try to create proxy
        try:
            proxy_name = prefix + ".Proxy"
            self.proxy = self.ic.propertyToProxy(proxy_name)
            if self.proxy:
                self.topic = True
        except Exception:
            self.topic = False
            
        if start and self.topic:
            self.start()

    def start(self):
        '''
        Starts the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        if not self.started and self.topic:
            self.running = True
            self.started = True
            self.thread = threading.Thread(target=self.update_pose3d)
            self.thread.start()

    def stop(self):
        '''
        Stops the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        if self.started:
            self.running = False
            if self.thread and self.thread.is_alive():
                self.thread.join()
            self.started = False

    def getPose3d(self):
        '''
        Returns last Pose3d. 

        @return last JdeRobotTypes Pose3d saved

        '''
        return self.pose3d

    def hasproxy(self):
        '''
        Returns if proxy has ben created or not. 

        @return if proxy has ben created or not (Boolean)

        '''
        return self.topic

    def update_pose3d(self):
        '''
        Internal method to update pose3d in a separate thread
        '''
        # This is a placeholder implementation
        # In a real implementation, this would interface with Ice to get pose3d data
        while self.running:
            try:
                # Simulate getting pose3d data from Ice interface
                # self.pose3d = get_pose3d_from_ice_interface(self.proxy)
                time.sleep(0.05)  # 20 Hz update rate
            except Exception:
                break