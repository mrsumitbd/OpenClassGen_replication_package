class LaserIceClient:
    '''
        Laser Ice Client. Recives LaserData from Ice interface running Laser update method in a thread.
    '''

    def __init__(self, ic, prefix, start=False):
        '''
            LaserIceClient Constructor.

            @param ic: Ice Communicator
            @param prefix: prefix name of client in config file
            @param start: indicates if start automatically the client

            @type ic: Ice Communicator
            @type prefix: String
            @type start: Boolean
        '''
        self.ic = ic
        self.props = ic.getProperties()
        try:
            proxy_str = self.props.getProperty(prefix + ".Proxy")
        except Ice.PropertyException:
            proxy_str = ""
        self._proxy = None
        if proxy_str:
            self._proxy = Ice.stringToProxy(proxy_str)
            # If you have a specific Slice-generated proxy class, use checkedCast here:
            # from Laser import LaserPrx
            # self._proxy = LaserPrx.checkedCast(self._proxy)
        self._thread = None
        self._running = False
        self._lock = threading.Lock()
        self._laserData = None
        if start:
            self.start()

    def start(self):
        '''
            Starts the client. If client is stopped you can not start again, Threading.Thread raised error
        '''
        if not self._proxy:
            raise RuntimeError("Proxy has not been created")
        if self._running:
            raise RuntimeError("Client already started")
        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def _run(self):
        while self._running:
            try:
                # Assuming the proxy has a method getLaserData()
                data = self._proxy.getLaserData()
                with self._lock:
                    self._laserData = data
            except Exception:
                pass
            time.sleep(0.01)

    def stop(self):
        '''
            Stops the client. If client is stopped you can not start again, Threading.Thread raised error
        '''
        if not self._running:
            raise RuntimeError("Client is not running")
        self._running = False
        if self._thread:
            self._thread.join()
            self._thread = None

    def getLaserData(self):
        '''
            Returns last LaserData.

            @return last JdeRobotTypes LaserData saved
        '''
        with self._lock:
            return self._laserData

    def hasproxy(self):
        '''
            Returns if proxy has been created or not.

            @return if proxy has been created or not (Boolean)
        '''
        return self._proxy is not None