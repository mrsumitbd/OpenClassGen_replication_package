class WCSCapabilitiesReader(object):
    '''Read and parses WCS capabilities document into a lxml.etree infoset
    '''

    def __init__(self, version=None, cookies=None, auth=None, timeout=30, headers=None):
        '''Initialize
        @type version: string
        @param version: WCS Version parameter e.g '1.0.0'
        '''
        self.version = version or '1.0.0'
        self.cookies = cookies
        self.auth = auth
        self.timeout = timeout
        self.headers = headers or {}

    def capabilities_url(self, service_url):
        '''Return a capabilities url
        @type service_url: string
        @param service_url: base url of WCS service
        @rtype: string
        @return: getCapabilities URL
        '''
        params = {
            'service': 'WCS',
            'version': self.version,
            'request': 'GetCapabilities'
        }
        
        if '?' in service_url:
            separator = '&'
        else:
            separator = '?'
            
        query_string = urllib.parse.urlencode(params)
        return service_url + separator + query_string

    def read(self, service_url, timeout=30):
        '''Get and parse a WCS capabilities document, returning an
        elementtree tree

        @type service_url: string
        @param service_url: The base url, to which is appended the service,
        version, and request parameters
        @rtype: elementtree tree
        @return: An elementtree tree representation of the capabilities document
        '''
        capabilities_url = self.capabilities_url(service_url)
        
        request = urllib.request.Request(capabilities_url, headers=self.headers)
        
        if self.auth:
            import base64
            credentials = base64.b64encode(f"{self.auth[0]}:{self.auth[1]}".encode()).decode()
            request.add_header('Authorization', f'Basic {credentials}')
        
        if self.cookies:
            cookie_string = '; '.join([f"{k}={v}" for k, v in self.cookies.items()])
            request.add_header('Cookie', cookie_string)
        
        with urllib.request.urlopen(request, timeout=timeout or self.timeout) as response:
            content = response.read()
        
        return etree.fromstring(content)

    def readString(self, st):
        '''Parse a WCS capabilities document, returning an
        instance of WCSCapabilitiesInfoset
        string should be an XML capabilities document
        '''
        return etree.fromstring(st.encode() if isinstance(st, str) else st)