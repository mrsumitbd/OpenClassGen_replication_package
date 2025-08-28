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
        self.subscriber = None
        self._last_data = None

    def __callback(self, event):
        '''
            Callback function to receive and save Bumper Scans. 

            @param event: ROS BumperScan received
            @type event: BumperScan
        '''
        self._last_data = event

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
            self.subscriber = rospy.Subscriber(self.topic,
                                               BumperData,
                                               self.__callback)

    def getBumperData(self):
        '''
            Returns last BumperData. 

            @return last JdeRobotTypes BumperData saved
        '''
        return self._last_data