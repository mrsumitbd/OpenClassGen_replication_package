class BaseAuth:
    ''' A base authentication class.

        All authentication modules should extend this class.
    '''

    def __init__(self, username, password, authoritative_source, auth_backend, auth_options=None):
        ''' Constructor.

            Note that the instance variables not are set by the constructor but
            by the :func:`authenticate` method. Therefore, run the
            :func:`authenticate`-method before trying to access those
            variables!

            * `username` [string]
                Username to authenticate as.
            * `password` [string]
                Password to authenticate with.
            * `authoritative_source` [string]
                Authoritative source of the query.
            * `auth_backend` [string]
                Name of authentication backend.
            * `auth_options` [dict]
                A dict which, if authenticated as a trusted user, can override
                `username` and `authoritative_source`.
        '''
        self.username = username
        self.password = password
        self.authoritative_source = authoritative_source
        self.auth_backend = auth_backend
        self.auth_options = auth_options if auth_options is not None else {}
        self.authenticated = False
        self.authorized = False

    def authenticate(self):
        ''' Verify authentication.

            Returns True/False dependant on whether the authentication
            succeeded or not.
        '''
        raise NotImplementedError("Subclasses must implement authenticate method")

    def authorize(self):
        ''' Verify authorization.

            Check if a user is authorized to perform a specific operation.
        '''
        raise NotImplementedError("Subclasses must implement authorize method")