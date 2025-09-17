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
        from slack_sdk import WebClient
        from slack_sdk.rtm import RTMClient
        
        self.slack_api = WebClient(token=self.token)
        rtm_client = RTMClient(token=self.token)
        
        @rtm_client.on('message')
        def handle_message(**payload):
            data = payload.get('data', {})
            if data.get('type') == 'message' and 'text' in data:
                self.channel_layer.send(self.channel_name, {
                    'type': 'slack.message',
                    'text': data['text'],
                    'channel': data.get('channel'),
                    'user': data.get('user'),
                    'ts': data.get('ts')
                })
        
        rtm_client.start()