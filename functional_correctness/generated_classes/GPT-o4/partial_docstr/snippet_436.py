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
        self.api_base = api_base.rstrip('/')
        self.session = requests.Session()
        self.current_team = RTMCurrentTeam(self)
        self.user = RTMUser(self)
        self.channel = RTMChannel(self)

    def start(self):
        '''Gets the rtm ws_host and user information

        Returns:
            None if request failed,
            else a dict containing "user"(User) and "ws_host"
        '''
        resp = self.get("rtm.start")
        if not getattr(resp, "ok", False):
            return None
        body = resp.json()
        return {
            "user": body.get("user"),
            "ws_host": body.get("ws_host")
        }

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
        url = "{}/{}".format(self.api_base, resource.lstrip('/'))
        params = {} if params is None else dict(params)
        params['token'] = self.token
        hdrs = {} if headers is None else dict(headers)
        r = self.session.request(method.upper(), url,
                                 params=params,
                                 data=data,
                                 json=json,
                                 headers=hdrs)
        return RTMResponse(r)

    def get(self, resource, params=None, headers=None):
        '''Sends a GET request

        Returns:
            RTMResponse
        '''
        return self.do(resource, "GET", params=params, headers=headers)

    def post(self, resource, data=None, json=None):
        '''Sends a POST request

        Returns:
            RTMResponse
        '''
        return self.do(resource, "POST", data=data, json=json)