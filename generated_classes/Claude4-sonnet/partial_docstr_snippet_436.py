class RTMClient(object):
    '''Real Time Message client

    Attributes:
        current_team(RTMCurrentTeam): service of current team
        user(RTMUser): service of current user
        channel(RTMChannel): service of current channel
    '''

    def __init__(self, token, api_base="https://rtm.bearychat.com"):
        '''
        Args:
            token(str): rtm token
            api_base(str): api url base
        '''
        self.token = token
        self.api_base = api_base
        self.current_team = RTMCurrentTeam(self)
        self.user = RTMUser(self)
        self.channel = RTMChannel(self)

    def start(self):
        '''Gets the rtm ws_host and user information

        Returns:
            None if request failed,
            else a dict containing "user"(User) and "ws_host"
        '''
        response = self.get("/start")
        if response.status_code == 200:
            return response.json()
        return None

    def do(self,
           resource,
           method,
           params=None,
           data=None,
           json=None,
           headers=None):
        '''Does the request job

        Args:
            resource(str): resource uri(relative path)
            method(str): HTTP method
            params(dict): uri queries
            data(dict): HTTP body(form)
            json(dict): HTTP body(json)
            headers(dict): HTTP headers

        Returns:
            RTMResponse
        '''
        url = self.api_base + resource
        if headers is None:
            headers = {}
        headers['Authorization'] = f'Bearer {self.token}'
        
        response = requests.request(
            method=method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers
        )
        return RTMResponse(response)

    def get(self, resource, params=None, headers=None):
        '''Sends a GET request

        Returns:
            RTMResponse
        '''
        return self.do(resource, 'GET', params=params, headers=headers)

    def post(self, resource, data=None, json=None):
        '''Sends a POST request

        Returns:
            RTMResponse
        '''
        return self.do(resource, 'POST', data=data, json=json)