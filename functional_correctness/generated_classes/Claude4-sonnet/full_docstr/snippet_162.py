class ListenerLaser:
    '''
        ROS Laser Subscriber. Laser Client to Receive Laser Scans from ROS nodes.
    '''

    def __init__(self, topic):
        '''
        ListenerLaser Constructor.

        @param topic: ROS topic to subscribe
        
        @type topic: String

        '''
        self.topic = topic
        self.sub = None
        self.laser_data = None
        self.lock = threading.Lock()

    def __callback(self, scan):
        '''
        Callback function to receive and save Laser Scans. 

        @param scan: ROS LaserScan received
        
        @type scan: LaserScan

        '''
        with self.lock:
            self.laser_data = scan

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
        if self.sub is None:
            self.sub = rospy.Subscriber(self.topic, LaserScan, self.__callback)

    def getLaserData(self):
        '''
        Returns last LaserData. 

        @return last JdeRobotTypes LaserData saved

        '''
        with self.lock:
            return self.laser_data