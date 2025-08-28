class Auth(object):
    '''
    Hold OAuth/Access Data, convenience methods.

    https://www.cronofy.com/developers/api/#authentication
    '''

    def __init__(self, client_id=None, client_secret=None,
                 access_token=None, refresh_token=None,
                 token_expiration=None):
        '''
        :param string client_id: OAuth Client ID. (Optional, default None)
        :param string client_secret: OAuth Client Secret. (Optional, default None)
        :param string access_token: Access Token for User's Account. (Optional, default None)
        :param string refresh_token: Existing Refresh Token for User's Account. (Optional, default None)
        :param datetime.datetime token_expiration: Datetime token expires. (Optional, default None)
        '''
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        if token_expiration and not isinstance(token_expiration, datetime):
            raise TypeError("token_expiration must be a datetime object")
        self.token_expiration = token_expiration

    def get_authorization(self):
        '''Get the authorization header with the currently active token

        :return: 'Authorization' header
        :rtype: ``string``
        '''
        if not self.access_token:
            raise RuntimeError("No access token available")
        return "Bearer {}".format(self.access_token)

    def get_api_key(self):
        '''Get the authorization header with the api key token

        :return: 'Authorization' header
        :rtype: ``string``
        '''
        if not self.client_secret:
            raise RuntimeError("No API key (client_secret) available")
        return "Bearer {}".format(self.client_secret)

    def update(self, **kwargs):
        '''Update fields

        :param KeywordArguments kwargs: Fields and values to update.
        '''
        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise AttributeError("Unknown field '{}'".format(key))
            setattr(self, key, value)