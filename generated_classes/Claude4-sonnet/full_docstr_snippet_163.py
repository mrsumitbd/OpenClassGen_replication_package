class Sonar:
    '''
        Sonar Connector. Recives LaserData from Ice interface when you run update method.
    '''

    def __init__(self, jdrc, prefix):
        '''
        Laser Contructor.
        Exits When it receives a Exception diferent to Ice.ConnectionRefusedException

        @param jdrc: Comm Communicator
        @param prefix: prefix name of client in config file

        @type ic: Ice Communicator
        @type prefix: String
        '''
        self.lock = threading.Lock()
        self.sonarData = jderobot.LaserData()
        self.proxy = None
        
        try:
            base = jdrc.getIceComm().stringToProxy(jdrc.getConfig().getProperty(prefix + ".Proxy"))
            self.proxy = jderobot.LaserPrx.checkedCast(base)
            if not self.proxy:
                raise Exception("Invalid proxy")
        except Ice.ConnectionRefusedException:
            print(prefix + ": connection refused")
        except Exception as e:
            print(prefix + ": " + str(e))
            exit(-1)

    def update(self):
        '''
        Updates LaserData.
        '''
        if self.hasproxy():
            try:
                self.lock.acquire()
                self.sonarData = self.proxy.getLaserData()
                self.lock.release()
            except Ice.Exception:
                self.lock.release()

    def hasproxy(self):
        '''
        Returns if proxy has ben created or not. 

        @return if proxy has ben created or not (Boolean)

        '''
        return self.proxy is not None

    def getSonarData(self):
        '''
        Returns last LaserData. 

        @return last JdeRobotTypes LaserData saved

        '''
        self.lock.acquire()
        sonarData = self.sonarData
        self.lock.release()
        return sonarData