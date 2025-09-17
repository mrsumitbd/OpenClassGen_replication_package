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
        base = service_url.rstrip('?&')
        delim = '?' if '?' not in base else '&'
        params = [('service', 'WCS'), ('request', 'GetCapabilities')]
        if self.version:
            params.append(('version', self.version))
        return base + delim + urlencode(params)

    def read(self, service_url, timeout=None):
        '''Get and parse a WCS capabilities document, returning an
        elementtree tree

        @type service_url: string
        @param service_url: The base url, to which is appended the service,
        version, and request parameters
        @rtype: elementtree tree
        @return: An elementtree tree representation of the capabilities document
        '''
        url = self.capabilities_url(service_url)
        to = timeout if timeout is not None else self.timeout
        resp = requests.get(url, headers=self.headers, cookies=self.cookies,
                            auth=self.auth, timeout=to)
        resp.raise_for_status()
        return self.readString(resp.content)

    def readString(self, st):
        '''Parse a WCS capabilities document, returning an
        instance of WCSCapabilitiesInfoset
        string should be an XML capabilities document
        '''
        if isinstance(st, str):
            st = st.encode('utf-8')
        parser = etree.XMLParser(ns_clean=True, recover=True)
        root = etree.fromstring(st, parser=parser)
        return etree.ElementTree(root)