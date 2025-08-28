class SQLClient(object):
    '''
    Allows you to send requests to CARTO's SQL API
    '''

    def __init__(self, auth_client, api_version='v2'):
        '''
        :param auth_client: Auth client to make authorized requests, such as
                            APIKeyAuthClient
        :param api_version: Current version is 'v2'. 'v1' can be used to avoid
                            caching, but it's not guaranteed to work
        :type auth_client: :class:`carto.auth.APIKeyAuthClient`
        :type api_version: str

        :return:
        '''
        self.auth_client = auth_client
        self.api_version = api_version
        self._base_url = '{0}/api/{1}/sql'.format(
            self.auth_client.base_url.rstrip('/'),
            self.api_version
        )

    def send(self, sql, parse_json=True, do_post=True, format=None, **request_args):
        '''
        Executes SQL query in a CARTO server

        :param sql: The SQL
        :param parse_json: Set it to False if you want raw reponse
        :param do_post: Set it to True to force post request
        :param format: Any of the data export formats allowed by CARTO's
                        SQL API
        :param request_args: Additional parameters to send with the request
        :type sql: str
        :type parse_json: boolean
        :type do_post: boolean
        :type format: str
        :type request_args: dictionary

        :return: response data, either as json or as a regular
                    response.content object
        :rtype: object

        :raise: CartoException
        '''
        params = {}
        if format is not None:
            params['format'] = format
        params.update(request_args)

        api_key = getattr(self.auth_client, 'api_key', None)
        if api_key:
            params['api_key'] = api_key

        if do_post:
            data = {'q': sql}
            resp = self.auth_client.session.post(self._base_url, params=params, data=data)
        else:
            params['q'] = sql
            resp = self.auth_client.session.get(self._base_url, params=params)

        try:
            resp.raise_for_status()
        except Exception:
            raise CartoException(resp)

        if parse_json:
            return resp.json()
        return resp.content