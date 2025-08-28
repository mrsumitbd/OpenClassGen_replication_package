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
        self.endpoint = ''

    def _build_path(self, *args):
        '''
        Build path with endpoint and args

        :param args: Tokens in the endpoint URL
        :type args: :py:class:`unicode`
        '''
        return '/'.join(str(arg) for arg in (self.endpoint,) + args)

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
        queryparams['offset'] = 0
        queryparams['count'] = 1000
        
        result = self._mc_client._get(url=url, **queryparams)
        
        for item in result.get(self._get_collection_name(), []):
            yield item
        
        total = result.get('total_items', 0)
        queryparams['offset'] += queryparams['count']
        
        while queryparams['offset'] < total:
            result = self._mc_client._get(url=url, **queryparams)
            for item in result.get(self._get_collection_name(), []):
                yield item
            queryparams['offset'] += queryparams['count']

    def _get_collection_name(self):
        '''
        Get the name of the collection for this endpoint
        '''
        # Default implementation - subclasses should override this
        return 'items'