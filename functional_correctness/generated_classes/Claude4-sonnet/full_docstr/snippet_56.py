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
        url = "{base_url}sql/{api_version}/".format(
            base_url=self.auth_client.base_url,
            api_version=self.api_version
        )
        
        params = {'q': sql}
        if format:
            params['format'] = format
        params.update(request_args)
        
        try:
            if do_post:
                response = self.auth_client.send(url, 'POST', params, None)
            else:
                response = self.auth_client.send(url, 'GET', params, None)
            
            if response.status_code != 200:
                raise CartoException("SQL API request failed with status code: {}".format(response.status_code))
            
            if parse_json:
                try:
                    return response.json()
                except ValueError:
                    return response.content
            else:
                return response.content
                
        except Exception as e:
            if isinstance(e, CartoException):
                raise
            raise CartoException("SQL API request failed: {}".format(str(e)))