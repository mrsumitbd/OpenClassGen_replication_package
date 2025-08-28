class API(object):
    '''Wrapper for vk.com API.'''

    def __init__(self, token=None, version='5.49', **kwargs):
        '''
        Override __init__.

        :param token (optional): `str` OAuth2 access token.
        :param version (optional): `str` API version.
        '''
        self.token = token
        self.version = version
        self.base_url = 'https://api.vk.com/method/'
        
    def get_url(self, method=None, **kwargs):
        '''Return url for call method.

        :param method (optional): `str` method name.
        :returns: `str` URL.
        '''
        params = kwargs.copy()
        if self.token:
            params['access_token'] = self.token
        params['v'] = self.version
        
        url = self.base_url + method
        if params:
            url += '?' + urlencode(params)
        return url
        
    def request(self, method, **kwargs):
        '''
        Send request to API.

        :param method: `str` method name.
        :returns: `dict` response.
        '''
        url = self.get_url(method, **kwargs)
        response = requests.get(url)
        return response.json()
        
    def __getattr__(self, attr):
        '''Override __getattr__.'''
        return APIMethod(self, attr)
        
    def __call__(self, **kwargs):
        '''Override __call__.'''
        pass