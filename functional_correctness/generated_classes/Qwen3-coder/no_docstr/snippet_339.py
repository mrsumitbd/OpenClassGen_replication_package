class LDAPServerSettings:
    def __init__(self, gssapi_factory):
        self._gssapi_factory = gssapi_factory
        self._gssapi = None

    @property
    def gssapi(self):
        if self._gssapi is None:
            self._gssapi = self._gssapi_factory()
        return self._gssapi