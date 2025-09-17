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
        self.method_name = kwargs.get('method_name', '')
        self.base_url = 'https://api.vk.com/method/'

    def get_url(self, method=None, **kwargs):
        '''Return url for call method.

        :param method (optional): `str` method name.
        :returns: `str` URL.
        '''
        if method:
            return self.base_url + method
        elif self.method_name:
            return self.base_url + self.method_name
        else:
            return self.base_url

    def request(self, method, **kwargs):
        '''
        Send request to API.

        :param method: `str` method name.
        :returns: `dict` response.
        '''
        url = self.get_url(method)
        params = kwargs.copy()
        params['v'] = self.version
        if self.token:
            params['access_token'] = self.token
        
        response = requests.get(url, params=params)
        return response.json()

    def __getattr__(self, attr):
        '''Override __getattr__.'''
        method_name = self.method_name + '.' + attr if self.method_name else attr
        return API(token=self.token, version=self.version, method_name=method_name)

    def __call__(self, **kwargs):
        '''Override __call__.'''
        return self.request(self.method_name, **kwargs)