class BaseFetchHandler(object):
    '''Base class for FetchHandler implementations in fetch plugins'''

    def can_handle(self, source):
        '''Returns True if the source can be handled. Otherwise returns
        a string explaining why it cannot'''
        return False, 'can_handle not implemented for source {}'.format(source)

    def install(self, source):
        '''Try to download and unpack the source. Return the path to the
        unpacked files or raise UnhandledSource.'''
        raise UnhandledSource('install not implemented for source {}'.format(source))

    def parse_url(self, url):
        return urllib.parse.urlparse(url)

    def base_url(self, url):
        '''Return url without querystring or fragment'''
        parts = self.parse_url(url)
        return urllib.parse.urlunparse((
            parts.scheme,
            parts.netloc,
            parts.path,
            parts.params,
            '',
            ''
        ))