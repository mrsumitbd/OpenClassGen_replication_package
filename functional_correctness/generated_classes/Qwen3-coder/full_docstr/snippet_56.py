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
        from carto.exceptions import CartoException
        import json

        # Prepare the request parameters
        params = dict(request_args)
        params['q'] = sql
        
        if format is not None:
            params['format'] = format

        try:
            if do_post:
                response = self.auth_client.send(self.auth_client.api_url + '/sql/' + self.api_version + '/sql', 'POST', data=params)
            else:
                response = self.auth_client.send(self.auth_client.api_url + '/sql/' + self.api_version + '/sql', 'GET', params=params)
            
            if response.status_code != 200:
                raise CartoException('HTTP error {}: {}'.format(response.status_code, response.text))
            
            if parse_json:
                return response.json()
            else:
                return response.content
                
        except Exception as e:
            if isinstance(e, CartoException):
                raise
            else:
                raise CartoException(e)