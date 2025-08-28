class IRIceClient:
    '''
        IR Ice Client. Recives LaserData from Ice interface running IR update method in a thread.
    '''

    def __init__(self, ic, prefix, start = False):
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
        self._proxy = None
        self._lastData = None
        self._lock = threading.Lock()
        self._thread = None
        self._running = False

        # try to create the proxy
        try:
            props = self.ic.getProperties()
            proxy_str = props.getProperty(self.prefix + ".Proxy")
            base = self.ic.stringToProxy(proxy_str)
            # you must replace 'Jderobot.IRPrx' with your actual IR proxy class
            self._proxy = Jderobot.IRPrx.checkedCast(base)
            if not self._proxy:
                raise RuntimeError("Invalid IR proxy")
        except Exception:
            self._proxy = None

        if start:
            self.start()

    def start(self):
        '''
            Starts the client. If client is stopped you can not start again, Threading.Thread raised error
        '''
        if not self.hasproxy():
            raise RuntimeError("Cannot start, proxy not initialized")
        if self._thread and self._thread.is_alive():
            raise RuntimeError("Client already started")
        self._running = True
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        '''
            Stops the client. If client is stopped you can not start again, Threading.Thread raised error
        '''
        if not self._thread or not self._thread.is_alive():
            return
        self._running = False
        self._thread.join()

    def getIRData(self):
        '''
            Returns last LaserData. 

            @return last JdeRobotTypes LaserData saved
        '''
        with self._lock:
            return self._lastData

    def hasproxy(self):
        '''
            Returns if proxy has ben created or not. 

            @return if proxy has ben created or not (Boolean)
        '''
        return self._proxy is not None

    def _run(self):
        while self._running:
            try:
                # replace 'update' with the actual method name of your IR interface
                data = self._proxy.update()
                with self._lock:
                    self._lastData = data
            except Exception:
                # ignore errors during update
                pass