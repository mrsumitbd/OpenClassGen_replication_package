class BaseApi(object):
    '''
    Simple class to buid path for entities
    '''

    def __init__(self, mc_client):
        '''
        Initialize the class with you user_id and secret_key

        :param mc_client: The mailchimp client connection
        :type mc_client: :mod:`mailchimp3.mailchimpclient.MailChimpClient`
        '''
        self._mc_client = mc_client

    def _build_path(self, *args):
        '''
        Build path with endpoint and args

        :param args: Tokens in the endpoint URL
        :type args: :py:class:`unicode`
        '''
        if hasattr(self, 'endpoint'):
            path_parts = [self.endpoint]
        else:
            path_parts = []
        
        for arg in args:
            if arg is not None:
                path_parts.append(str(arg))
        
        return '/'.join(path_parts)

    def _iterate(self, url, **queryparams):
        '''
        Iterate over all pages for the given url. Feed in the result of self._build_path as the url.

        :param url: The url of the endpoint
        :type url: :py:class:`str`
        :param queryparams: The query string parameters
        queryparams['fields'] = []
        queryparams['exclude_fields'] = []
        queryparams['count'] = integer
        queryparams['offset'] = integer
        '''
        offset = queryparams.get('offset', 0)
        count = queryparams.get('count', 10)
        
        while True:
            current_params = queryparams.copy()
            current_params['offset'] = offset
            current_params['count'] = count
            
            response = self._mc_client._get(url=url, **current_params)
            
            if not response or not isinstance(response, dict):
                break
                
            items_key = None
            for key in response.keys():
                if isinstance(response[key], list) and key != 'links':
                    items_key = key
                    break
            
            if not items_key or not response[items_key]:
                break
                
            for item in response[items_key]:
                yield item
                
            if len(response[items_key]) < count:
                break
                
            offset += count