class Client(object):
    '''A client library for pasteraw.

    To use pasteraw.com:

    >>> c = pasteraw.Client()
    >>> url = c.create_paste('Lorem ipsum.')
    >>> print(url)
    http://cdn.pasteraw.com/9lvwkwgrgji5gbhjygxgaqcfx3hefpb

    If you're using your own pasteraw deployment, pass your own API endpoint to
    the client:

    >>> c = pasteraw.Client('http://pasteraw.example.com/api/v1')

    '''

    def __init__(self, endpoint=None):
        '''Initialize a pasteraw client for the given endpoint (optional).'''
        base = endpoint.rstrip('/') if endpoint else 'https://pasteraw.com/api/v1'
        self.api_url = base + '/raw'
        p = urlparse(base)
        self.cdn_base = f'{p.scheme}://cdn.{p.netloc}'

    def create_paste(self, content):
        '''Create a raw paste of the given content.

        Returns a URL to the paste, or raises a ``pasteraw.Error`` if something
        tragic happens instead.

        '''
        headers = {'Content-Type': 'text/plain'}
        resp = requests.post(self.api_url, data=content.encode('utf-8'), headers=headers)
        if resp.status_code >= 400:
            raise Error(f'HTTP {resp.status_code}: {resp.text}')
        key = resp.text.strip()
        return f'{self.cdn_base}/{key}'