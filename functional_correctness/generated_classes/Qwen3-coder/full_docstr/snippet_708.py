class WMSCapabilitiesReader(object):
    '''Read and parse capabilities document into a lxml.etree infoset
    '''

    def __init__(self, version='1.1.1', url=None, un=None, pw=None, headers=None, auth=None):
        '''Initialize'''
        self.version = version
        self.url = url
        self.username = un
        self.password = pw
        self.headers = headers or {}
        self.auth = auth

    def capabilities_url(self, service_url):
        '''Return a capabilities url
        '''
        parsed_url = urllib.parse.urlparse(service_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # Add or update required parameters
        query_params['service'] = ['WMS']
        query_params['version'] = [self.version]
        query_params['request'] = ['GetCapabilities']
        
        # Reconstruct the query string
        query_string = urllib.parse.urlencode(query_params, doseq=True)
        
        # Reconstruct the URL
        new_parsed = parsed_url._replace(query=query_string)
        return urllib.parse.urlunparse(new_parsed)

    def read(self, service_url, timeout=30):
        '''Get and parse a WMS capabilities document, returning an
        elementtree instance

        service_url is the base url, to which is appended the service,
        version, and request parameters
        '''
        cap_url = self.capabilities_url(service_url)
        
        # Create request with headers
        request = urllib.request.Request(cap_url, headers=self.headers)
        
        # Handle authentication if provided
        if self.username and self.password:
            # Create password manager
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(None, cap_url, self.username, self.password)
            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            opener = urllib.request.build_opener(handler)
            response = opener.open(request, timeout=timeout)
        else:
            response = urllib.request.urlopen(request, timeout=timeout)
        
        # Parse the XML response
        return etree.parse(response)

    def readString(self, st):
        '''Parse a WMS capabilities document, returning an elementtree instance.

        string should be an XML capabilities document
        '''
        return etree.fromstring(st.encode('utf-8') if isinstance(st, str) else st)