class SonarIceClient:
    '''
        Sonar Ice Client. Recives LaserData from Ice interface running Sonar update method in a thread.
    '''

    def __init__(self, ic, prefix, start=False):
        self.ic = ic
        self.prefix = prefix
        self._sonarData = None
        self._running = False
        self._thread = threading.Thread(target=self._update_loop)
        self._thread.daemon = True

        props = ic.getProperties()
        proxy_str = props.getProperty(prefix + ".Proxy")
        self.proxy = SonarPrx.checkedCast(ic.stringToProxy(proxy_str))
        if not self.proxy:
            raise RuntimeError("Invalid proxy: " + proxy_str)

        period_ms = props.getProperty(prefix + ".Period", "100")
        try:
            self._period = float(period_ms) / 1000.0
        except:
            self._period = 0.1

        if start:
            self.start()

    def _update_loop(self):
        while self._running:
            try:
                self._sonarData = self.proxy.getSonarData()
            except Ice.Exception:
                pass
            time.sleep(self._period)

    def start(self):
        self._running = True
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()

    def getSonarData(self):
        return self._sonarData

    def hasproxy(self):
        return self.proxy is not None