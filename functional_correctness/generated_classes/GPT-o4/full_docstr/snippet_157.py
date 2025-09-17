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
        props = ic.getProperties()
        proxy_prop = props.getProperty(prefix + ".Proxy")
        prx = ic.propertyToProxy(prefix + ".Proxy")
        self.proxy = JdeRobotTypes.Pose3dPrx.checkedCast(prx)
        if not self.proxy:
            raise RuntimeError("Invalid proxy for {}".format(proxy_prop))
        period_str = props.getProperty(prefix + ".Period", "100")
        try:
            self.period = int(period_str)
        except ValueError:
            self.period = 100
        self._pose = None
        self._run = False
        self._thread = None
        if start:
            self.start()

    def start(self):
        '''
            Starts the client. If client is stopped you can not start again, Threading.Thread raised error
        '''
        if self._thread is None:
            self._thread = threading.Thread(target=self._run_loop)
            self._thread.daemon = True
            self._run = True
        self._thread.start()

    def stop(self):
        '''
            Stops the client. If client is stopped you can not start again, Threading.Thread raised error
        '''
        self._run = False
        if self._thread:
            self._thread.join()

    def getPose3d(self):
        '''
            Returns last Pose3d. 

            @return last JdeRobotTypes Pose3d saved
        '''
        return self._pose

    def hasproxy(self):
        '''
            Returns if proxy has ben created or not. 

            @return if proxy has ben created or not (Boolean)
        '''
        return self.proxy is not None

    def _run_loop(self):
        while self._run:
            try:
                p = self.proxy.getPose3d()
                self._pose = p
            except Ice.Exception:
                pass
            time.sleep(self.period / 1000.0)