class BaseFetchHandler(object):
    '''Base class for FetchHandler implementations in fetch plugins'''

    def can_handle(self, source):
        '''Returns True if the source can be handled. Otherwise returns
        a string explaining why it cannot'''
        pass

    def install(self, source):
        '''Try to download and unpack the source. Return the path to the
        unpacked files or raise UnhandledSource.'''
        pass

    def parse_url(self, url):
        pass

    def base_url(self, url):
        '''Return url without querystring or fragment'''
        pass