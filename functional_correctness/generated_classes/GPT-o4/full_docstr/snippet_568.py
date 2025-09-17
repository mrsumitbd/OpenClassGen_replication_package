class NominatimRequest(object):
    '''
    Abstract base class for connections to a Nominatim instance
    '''

    def __init__(self, base_url=None):
        '''
        Provide logging and set the Nominatim instance
        (defaults to http://nominatim.openstreetmap.org )
        '''
        self.logger = logging.getLogger(self.__class__.__name__)
        self.base_url = base_url or 'http://nominatim.openstreetmap.org'

    def request(self, url):
        '''
        Send a http request to the given *url*, try to decode
        the reply assuming it's JSON in UTF-8, and return the result

        :returns: Decoded result, or None in case of an error
        :rtype: mixed
        '''
        try:
            self.logger.debug("Requesting URL: %s", url)
            with urllib.request.urlopen(url) as response:
                raw = response.read()
            text = raw.decode('utf-8')
            return json.loads(text)
        except Exception as e:
            self.logger.error("Error fetching URL %s: %s", url, e)
            return None