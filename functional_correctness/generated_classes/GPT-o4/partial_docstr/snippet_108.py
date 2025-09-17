class CORSMiddleware:
    '''This is the middleware that applies a CORS object to requests.

    Args:
        cors (CORS, required): An instance of :py:class:`~falcon.cors.CORS`.
        default_enabled (bool, optional): Whether CORS processing should
            take place for every resource.  Default ``True``.
    '''

    def __init__(self, cors, default_enabled=True):
        self.cors = cors
        self.default_enabled = default_enabled

    def process_resource(self, req, resp, resource, *args):
        # Determine whether CORS is enabled for this resource
        enabled = getattr(resource, 'cors_enabled', None)
        if enabled is None:
            enabled = self.default_enabled

        if enabled:
            # Delegate to the CORS object
            self.cors.process_request(req, resp)