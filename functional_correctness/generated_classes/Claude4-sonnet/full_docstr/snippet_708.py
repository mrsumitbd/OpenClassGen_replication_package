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
        params = {
            'service': 'WMS',
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
        '''Get and parse a WMS capabilities document, returning an
        elementtree instance

        service_url is the base url, to which is appended the service,
        version, and request parameters
        '''
        capabilities_url = self.capabilities_url(service_url)
        
        request = urllib.request.Request(capabilities_url)
        
        for key, value in self.headers.items():
            request.add_header(key, value)
            
        if self.username and self.password:
            import base64
            credentials = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            request.add_header('Authorization', f'Basic {credentials}')
        
        if self.auth:
            request.add_header('Authorization', self.auth)
            
        response = urllib.request.urlopen(request, timeout=timeout)
        content = response.read()
        
        return etree.fromstring(content)

    def readString(self, st):
        '''Parse a WMS capabilities document, returning an elementtree instance.

        string should be an XML capabilities document
        '''
        return etree.fromstring(st.encode() if isinstance(st, str) else st)