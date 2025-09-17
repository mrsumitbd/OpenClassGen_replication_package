class Client(object):
    '''
    Main client to instantiate the SlackAPI and client factory
    '''

    def __init__(self, channel_layer, token, channel_name=u'slack.send'):
        '''
        Args:
            channel_layer: channel layer on which this client will communicate to Django
            token: {str} Slack token
            channel_name: {str} channel name to send messages that will come back to slack
        '''
        self.channel_layer = channel_layer
        self.token = token
        self.channel_name = channel_name
        self._send = async_to_sync(self.channel_layer.send)

    def run(self):
        '''
        Main interface. Instantiate the SlackAPI, connect to RTM
        and start the client.
        '''
        sc = SlackClient(self.token)
        if not sc.rtm_connect():
            raise RuntimeError("Unable to connect to Slack RTM")
        while True:
            for event in sc.rtm_read():
                self._send(self.channel_name, {
                    "type": "slack.event",
                    "event": event
                })
            time.sleep(1)