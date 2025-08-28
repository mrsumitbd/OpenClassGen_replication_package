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
        self.jdrc = jdrc
        self.prefix = prefix
        self.proxy = None
        self.sonarData = None
        self.hasproxyflag = False
        
        try:
            self.proxy = self.jdrc.getProxy(self.prefix)
            if self.proxy:
                self.hasproxyflag = True
        except Ice.ConnectionRefusedException:
            pass
        except Exception as e:
            exit()

    def update(self):
        '''
        Updates LaserData.
        '''
        if self.hasproxy() and self.proxy:
            try:
                self.sonarData = self.proxy.getLaserData()
            except Ice.ConnectionRefusedException:
                pass
            except Exception as e:
                exit()

    def hasproxy(self):
        '''
        Returns if proxy has ben created or not. 

        @return if proxy has ben created or not (Boolean)

        '''
        return self.hasproxyflag

    def getSonarData(self):
        '''
        Returns last LaserData. 

        @return last JdeRobotTypes LaserData saved

        '''
        return self.sonarData