class BaseFetchHandler(object):
    '''Base class for FetchHandler implementations in fetch plugins'''

    def can_handle(self, source):
        '''Returns True if the source can be handled. Otherwise returns
        a string explaining why it cannot'''
        return "Base handler cannot handle any sources"

    def install(self, source):
        '''Try to download and unpack the source. Return the path to the
        unpacked files or raise UnhandledSource.'''
        raise NotImplementedError("Subclasses must implement install method")

    def parse_url(self, url):
        from urllib.parse import urlparse
        return urlparse(url)

    def base_url(self, url):
        '''Return url without querystring or fragment'''
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(url)
        return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))