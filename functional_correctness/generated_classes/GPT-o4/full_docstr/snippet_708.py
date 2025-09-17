class WMSCapabilitiesReader(object):
    '''Read and parse capabilities document into a lxml.etree infoset
    '''

    def __init__(self, version='1.1.1', url=None, un=None, pw=None, headers=None, auth=None):
        '''Initialize'''
        self.version = version
        self.url = url
        self.headers = headers
        if auth is not None:
            self.auth = auth
        elif un is not None and pw is not None:
            self.auth = (un, pw)
        else:
            self.auth = None

    def capabilities_url(self, service_url):
        '''Return a capabilities url'''
        parsed = urlparse(service_url)
        qs = dict(parse_qsl(parsed.query))
        qs.update({
            'service': 'WMS',
            'version': self.version,
            'request': 'GetCapabilities'
        })
        new_query = urlencode(qs)
        return urlunparse((
            parsed.scheme,
            parsed.netloc,
            parsed.path,
            parsed.params,
            new_query,
            parsed.fragment
        ))

    def read(self, service_url, timeout=30):
        '''Get and parse a WMS capabilities document, returning an
        elementtree instance

        service_url is the base url, to which is appended the service,
        version, and request parameters
        '''
        url = self.capabilities_url(service_url)
        resp = requests.get(url, headers=self.headers, auth=self.auth, timeout=timeout)
        resp.raise_for_status()
        parser = etree.XMLParser(ns_clean=True, recover=True)
        root = etree.fromstring(resp.content, parser=parser)
        return etree.ElementTree(root)

    def readString(self, st):
        '''Parse a WMS capabilities document, returning an elementtree instance.

        string should be an XML capabilities document
        '''
        data = st.encode('utf-8') if isinstance(st, str) else st
        parser = etree.XMLParser(ns_clean=True, recover=True)
        root = etree.fromstring(data, parser=parser)
        return etree.ElementTree(root)