class ListenerBumper:
    '''
        ROS Bumper Subscriber. Bumper Client to Receive Bumper Scans from ROS nodes.
    '''

    def __init__(self, topic):
        '''
        ListenerBumper Constructor.

        @param topic: ROS topic to subscribe
        
        @type topic: String

        '''
        self.topic = topic
        self.sub = None
        self.bumperData = None
        self.lock = threading.Lock()

    def __callback(self, event):
        '''
        Callback function to receive and save Bumper Scans. 

        @param event: ROS BumperScan received
        
        @type event: BumperScan

        '''
        with self.lock:
            self.bumperData = event

    def stop(self):
        '''
        Stops (Unregisters) the client.

        '''
        if self.sub is not None:
            self.sub.unregister()
            self.sub = None

    def start(self):
        '''
        Starts (Subscribes) the client.

        '''
        self.sub = rospy.Subscriber(self.topic, BumperEvent, self.__callback)

    def getBumperData(self):
        '''
        Returns last BumperData. 

        @return last JdeRobotTypes BumperData saved

        '''
        with self.lock:
            return self.bumperData