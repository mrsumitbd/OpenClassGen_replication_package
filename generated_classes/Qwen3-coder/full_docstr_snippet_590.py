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
        self.slack_api = None

    def run(self):
        '''
        Main interface. Instantiate the SlackAPI, connect to RTM
        and start the client.
        '''
        from slack import WebClient
        from slack.rtm.client import RTMClient
        
        # Instantiate the Slack API client
        self.slack_api = WebClient(token=self.token)
        
        # Create RTM client
        rtm_client = RTMClient(token=self.token)
        
        # Start the RTM client
        rtm_client.start()