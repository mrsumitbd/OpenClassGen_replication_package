class CORSMiddleware:
    '''This is the middleware that applies a CORS object to requests.

    Args:
        cors (CORS, required): An instance of :py:class:`~falcon.cors.CORS`.
        default_enabled (bool, optional): Whether CORS processing should
            take place for every resource.  Default ``True``.
    '''

    def __init__(self, cors, default_enabled=True):
        self._cors = cors
        self._default_enabled = default_enabled

    def process_resource(self, req, resp, resource, *args):
        cors_enabled = getattr(resource, 'cors_enabled', self._default_enabled)
        if cors_enabled:
            self._cors.process_resource(req, resp, resource, *args)