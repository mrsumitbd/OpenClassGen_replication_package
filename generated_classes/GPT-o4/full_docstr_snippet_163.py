class Sonar:
    '''
        Sonar Connector. Receives LaserData from Ice interface when you run update method.
    '''

    def __init__(self, jdrc, prefix):
        '''
            Laser Constructor.
            Exits when it receives an exception different from Ice.ConnectionRefusedException

            @param jdrc: Ice Communicator
            @param prefix: prefix name of client in config file
        '''
        self._data = None
        try:
            props = jdrc.getProperties()
            proxy_str = props.getProperty(prefix + ".Proxy")
            base = jdrc.stringToProxy(proxy_str)
            self._proxy = JdeRobot.SonarPrx.ice_checkedCast(base)
        except Ice.ConnectionRefusedException:
            self._proxy = None
        except Exception:
            sys.exit(1)

    def update(self):
        '''
            Updates LaserData.
        '''
        if not self.hasproxy():
            return
        try:
            self._data = self._proxy.getLaserData()
        except Exception:
            self._data = None

    def hasproxy(self):
        '''
            Returns if proxy has been created or not.
            @return Boolean
        '''
        return self._proxy is not None

    def getSonarData(self):
        '''
            Returns last LaserData.
            @return JdeRobotTypes.LaserData
        '''
        return self._data