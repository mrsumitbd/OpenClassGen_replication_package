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
        if endpoint is None:
            self.endpoint = 'https://pasteraw.com/api/v1'
        else:
            self.endpoint = endpoint.rstrip('/')

    def create_paste(self, content):
        '''Create a raw paste of the given content.

        Returns a URL to the paste, or raises a ``pasteraw.Error`` if something
        tragic happens instead.

        '''
        try:
            response = requests.post(
                f'{self.endpoint}/paste',
                data={'content': content},
                timeout=30
            )
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    return data.get('url')
                except (json.JSONDecodeError, KeyError):
                    raise Error('Invalid response format from server')
            else:
                raise Error(f'HTTP {response.status_code}: {response.text}')
                
        except requests.exceptions.RequestException as e:
            raise Error(f'Request failed: {str(e)}')