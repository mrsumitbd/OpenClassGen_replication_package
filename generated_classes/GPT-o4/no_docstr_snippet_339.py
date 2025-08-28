class LDAPServerSettings:
    def __init__(self, gssapi_factory):
        if not callable(gssapi_factory):
            raise TypeError("gssapi_factory must be callable")
        self._gssapi_factory = gssapi_factory
        self._gssapi_instance = None

    @property
    def gssapi(self):
        if self._gssapi_instance is None:
            self._gssapi_instance = self._gssapi_factory()
        return self._gssapi_instance