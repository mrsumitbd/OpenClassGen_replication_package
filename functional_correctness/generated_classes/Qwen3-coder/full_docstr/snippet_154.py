class LaserIceClient:
    '''
        Laser Ice Client. Recives LaserData from Ice interface running Laser update method in a thread.
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
        self.laser_proxy = None
        self.laser_data = None
        self.running = False
        self.thread = None
        self.lock = threading.Lock()
        
        # Try to create proxy
        try:
            proxy_name = prefix + ".Proxy"
            self.laser_proxy = self.ic.propertyToProxy(proxy_name)
            if self.laser_proxy:
                # Assuming JdeRobotTypes.LaserPrx.checkedCast or similar
                # This would depend on the actual Ice interface
                self.laser_proxy = self.laser_proxy  # Placeholder
        except Exception:
            self.laser_proxy = None
            
        if start:
            self.start()

    def start(self):
        '''
        Starts the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        if self.thread is not None and self.thread.is_alive():
            return
            
        if self.laser_proxy is None:
            raise Exception("No proxy available to start client")
            
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        '''
        Stops the client. If client is stopped you can not start again, Threading.Thread raised error

        '''
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

    def getLaserData(self):
        '''
        Returns last LaserData. 

        @return last JdeRobotTypes LaserData saved

        '''
        with self.lock:
            return self.laser_data

    def hasproxy(self):
        '''
        Returns if proxy has ben created or not. 

        @return if proxy has ben created or not (Boolean)

        '''
        return self.laser_proxy is not None

    def _run(self):
        '''
        Internal method to run in thread
        '''
        while self.running:
            try:
                if self.laser_proxy:
                    # Assuming getLaserData() method exists on proxy
                    # This would depend on the actual Ice interface
                    new_data = self.laser_proxy.getLaserData()
                    with self.lock:
                        self.laser_data = new_data
                time.sleep(0.05)  # 20 Hz update rate
            except Exception:
                # Handle connection errors or other exceptions
                time.sleep(0.1)