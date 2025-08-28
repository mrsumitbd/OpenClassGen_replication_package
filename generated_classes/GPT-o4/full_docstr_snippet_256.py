class BaseAuth(abc.ABC):
    ''' A base authentication class.

        All authentication modules should extend this class.
    '''

    def __init__(self, username, password, authoritative_source, auth_backend, auth_options=None):
        self._raw_username = username
        self._password = password
        self._raw_authoritative_source = authoritative_source
        self._auth_backend = auth_backend
        self._auth_options = auth_options or {}
        self.authenticated = False
        self.username = None
        self.authoritative_source = None

    @abc.abstractmethod
    def _authenticate_backend(self):
        """Return True if credential check against the backend succeeds."""
        raise NotImplementedError

    def authenticate(self):
        """Verify authentication against the backend and set instance variables."""
        ok = self._authenticate_backend()
        if not ok:
            self.authenticated = False
            return False
        self.authenticated = True
        # apply overrides if provided
        self.username = self._auth_options.get('username', self._raw_username)
        self.authoritative_source = self._auth_options.get(
            'authoritative_source',
            self._raw_authoritative_source
        )
        return True

    @abc.abstractmethod
    def authorize(self):
        """Return True/False depending on whether the user is authorized."""
        raise NotImplementedError