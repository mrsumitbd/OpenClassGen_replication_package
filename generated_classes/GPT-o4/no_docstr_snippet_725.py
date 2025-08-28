class PropResourceLink(object):
    def __init__(self, clsname):
        self.clsname = clsname

    def __call__(self, resource=None):
        base = f"/{self.clsname}"
        if resource is None:
            return base
        try:
            rid = resource.id
        except AttributeError:
            raise AttributeError(f"Resource passed to {self.clsname} link has no 'id' attribute")
        return f"{base}/{rid}"