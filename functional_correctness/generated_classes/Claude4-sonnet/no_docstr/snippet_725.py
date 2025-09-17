class PropResourceLink(object):
    def __init__(self, clsname):
        self.clsname = clsname

    def __call__(self, resource=None):
        def decorator(func):
            func._prop_resource_link = {
                'clsname': self.clsname,
                'resource': resource
            }
            return func
        return decorator