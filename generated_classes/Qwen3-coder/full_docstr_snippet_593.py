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
        self.endpoint = endpoint or 'https://pasteraw.com/api/v1'

    def create_paste(self, content):
        '''Create a raw paste of the given content.

        Returns a URL to the paste, or raises a ``pasteraw.Error`` if something
        tragic happens instead.

        '''
        try:
            response = requests.post(
                self.endpoint + '/pastes',
                data={'content': content},
                headers={'User-Agent': 'pasteraw.py'}
            )
            response.raise_for_status()
            data = response.json()
            return data['url']
        except requests.exceptions.RequestException as e:
            raise Error(str(e))
        except (KeyError, json.JSONDecodeError) as e:
            raise Error('Invalid response from server: {}'.format(str(e)))