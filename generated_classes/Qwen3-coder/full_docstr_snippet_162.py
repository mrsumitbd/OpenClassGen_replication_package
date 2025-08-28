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
        self.data = LaserData()
        self.sub = None
        self.start()

    def __callback(self, scan):
        '''
        Callback function to receive and save Laser Scans. 

        @param scan: ROS LaserScan received
        
        @type scan: LaserScan

        '''
        self.data.values = list(scan.ranges)
        self.data.minAngle = scan.angle_min
        self.data.maxAngle = scan.angle_max
        self.data.minRange = scan.range_min
        self.data.maxRange = scan.range_max
        self.data.angleIncrement = scan.angle_increment

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
        return self.data