class UriParam:
    '''Represents a URI value as a parameter to a SPARQL query'''

    def __init__(self, uri):
        '''
        Initialize the UriParam value
        :param uri: the uri value to wrap
        '''
        if not isinstance(uri, str):
            raise TypeError(f"URI must be a string, got {type(uri).__name__}")
        if not uri:
            raise ValueError("URI cannot be an empty string")
        self.uri = uri

    def __repr__(self):
        '''
        The official string representation for the URI
        :return: the string representation for the URI
        '''
        return f"<{self.uri}>"