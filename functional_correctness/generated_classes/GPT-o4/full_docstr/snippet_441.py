class API(object):
    '''Wrapper for vk.com API.'''

    def __init__(self, token=None, version='5.49', **kwargs):
        """
        Override __init__.

        :param token (optional): `str` OAuth2 access token.
        :param version (optional): `str` API version.
        """
        self.token = token
        self.version = version
        self.base_url = 'https://api.vk.com/method'
        self._session = requests.Session()
        self._method = None

    def get_url(self, method=None, **kwargs):
        '''Return url for call method.

        :param method (optional): `str` method name.
        :returns: `str` URL.
        '''
        m = method or self._method or ''
        url = f"{self.base_url}/{m}"
        params = {}
        if self.token:
            params['access_token'] = self.token
        params['v'] = self.version
        params.update(kwargs)
        query = urlencode(params, doseq=True)
        return f"{url}?{query}"

    def request(self, method, **kwargs):
        '''
        Send request to API.

        :param method: `str` method name.
        :returns: `dict` response.
        '''
        url = self.get_url(method, **kwargs)
        resp = self._session.get(url)
        resp.raise_for_status()
        data = resp.json()
        if 'error' in data:
            err = data['error']
            code = err.get('error_code')
            msg = err.get('error_msg')
            raise Exception(f"VK API error {code}: {msg}")
        return data.get('response', data)

    def __getattr__(self, attr):
        '''Override __getattr__.'''
        if attr.startswith('_'):
            raise AttributeError(attr)
        new = self.__class__(token=self.token, version=self.version)
        new._session = self._session
        if self._method:
            new._method = f"{self._method}.{attr}"
        else:
            new._method = attr
        return new

    def __call__(self, **kwargs):
        '''Override __call__.'''
        if not self._method:
            raise ValueError("API method is not specified")
        return self.request(self._method, **kwargs)