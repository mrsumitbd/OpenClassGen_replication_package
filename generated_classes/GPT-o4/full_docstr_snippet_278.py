class BaseApi(object):
    '''
    Simple class to build path for entities
    '''

    def __init__(self, mc_client):
        '''
        Initialize the class with your MailChimp client

        :param mc_client: The mailchimp client connection
        :type mc_client: :mod:`mailchimp3.mailchimpclient.MailChimpClient`
        '''
        self.mc_client = mc_client

    def _build_path(self, *args):
        '''
        Build path with endpoint and args

        :param args: Tokens in the endpoint URL
        :type args: :py:class:`unicode`
        '''
        parts = [str(arg).strip('/') for arg in args if arg is not None]
        return '/'.join(parts)

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
        params = queryparams.copy()
        offset = params.get('offset', 0)
        count = params.get('count', 1000)
        params['offset'] = offset
        params['count'] = count

        all_items = []
        total_items = None

        while True:
            response = self.mc_client._get(url, **params)
            if total_items is None:
                total_items = response.get('total_items', 0)

            # find the list in the response
            items_key = next((k for k, v in response.items() if isinstance(v, list)), None)
            if not items_key:
                break

            items = response.get(items_key, [])
            all_items.extend(items)

            offset += count
            if offset >= total_items:
                break
            params['offset'] = offset

        return all_items