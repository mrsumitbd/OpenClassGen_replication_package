class WCSCapabilitiesReader(object):
    '''Read and parses WCS capabilities document into a lxml.etree infoset
    '''

    def __init__(self, version=None, cookies=None, auth=None, timeout=30, headers=None):
        '''Initialize
        @type version: string
        @param version: WCS Version parameter e.g '1.0.0'
        '''
        self.version = version
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
        # Parse the service URL to handle existing query parameters
        parsed_url = urllib.parse.urlparse(service_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # Add or update WCS parameters
        query_params['service'] = 'WCS'
        if self.version:
            query_params['version'] = self.version
        query_params['request'] = 'GetCapabilities'
        
        # Reconstruct the query string
        query_string = urllib.parse.urlencode(query_params, doseq=True)
        
        # Reconstruct the full URL
        new_url = urllib.parse.urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            query_string,
            parsed_url.fragment
        ))
        
        return new_url

    def read(self, service_url, timeout=30):
        '''Get and parse a WCS capabilities document, returning an
        elementtree tree

        @type service_url: string
        @param service_url: The base url, to which is appended the service,
        version, and request parameters
        @rtype: elementtree tree
        @return: An elementtree tree representation of the capabilities document
        '''
        # Get the capabilities URL
        url = self.capabilities_url(service_url)
        
        # Create request with headers
        request = urllib.request.Request(url, headers=self.headers)
        
        # Handle authentication if provided
        if self.auth:
            # Add authentication handler
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, url, self.auth[0], self.auth[1])
            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            opener = urllib.request.build_opener(handler)
            urllib.request.install_opener(opener)
        
        # Make the request
        response = urllib.request.urlopen(request, timeout=timeout)
        
        # Parse the response
        return etree.parse(response)

    def readString(self, st):
        '''Parse a WCS capabilities document, returning an
        instance of WCSCapabilitiesInfoset
        string should be an XML capabilities document
        '''
        # Parse the XML string directly
        return etree.parse(io.StringIO(st))