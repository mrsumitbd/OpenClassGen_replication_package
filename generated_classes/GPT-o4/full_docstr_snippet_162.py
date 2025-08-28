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
        self.subscriber = None
        self.laserData = None

    def __callback(self, scan):
        '''
        Callback function to receive and save Laser Scans.

        @param scan: ROS LaserScan received

        @type scan: LaserScan
        '''
        data = LaserData()
        data.distances = list(scan.ranges)
        data.angle0 = scan.angle_min
        data.aperture = scan.angle_max - scan.angle_min
        data.resolution = scan.angle_increment
        data.count = len(scan.ranges)
        self.laserData = data

    def stop(self):
        '''
        Stops (Unregisters) the client.
        '''
        if self.subscriber is not None:
            self.subscriber.unregister()
            self.subscriber = None

    def start(self):
        '''
        Starts (Subscribes) the client.
        '''
        if self.subscriber is None:
            self.subscriber = rospy.Subscriber(self.topic, LaserScan, self.__callback)

    def getLaserData(self):
        '''
        Returns last LaserData.

        @return last JdeRobotTypes LaserData saved
        '''
        return self.laserData