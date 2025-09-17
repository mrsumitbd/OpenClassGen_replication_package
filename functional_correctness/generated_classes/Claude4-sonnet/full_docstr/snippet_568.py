class NominatimRequest(object):
    '''
    Abstract base class for connections to a Nominatim instance
    '''

    def __init__(self, base_url=None):
        '''
        Provide logging and set the Nominatim instance
        (defaults to http://nominatim.openstreetmap.org )
        '''
        self.logger = logging.getLogger(__name__)
        if base_url is None:
            self.base_url = "http://nominatim.openstreetmap.org"
        else:
            self.base_url = base_url

    def request(self, url):
        '''
        Send a http request to the given *url*, try to decode
        the reply assuming it's JSON in UTF-8, and return the result

        :returns: Decoded result, or None in case of an error
        :rtype: mixed
        '''
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read().decode('utf-8')
                return json.loads(data)
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, UnicodeDecodeError) as e:
            self.logger.error(f"Request failed: {e}")
            return None