class User(object):
    '''Represent a CircleCI authenticated user.

    Attributes:
        client: An instance of CircleClient object.
    '''

    def __init__(self, client):
        self.client = client

    def info(self):
        '''Return information about the user as a dictionary.'''
        return self.client.get('/me')