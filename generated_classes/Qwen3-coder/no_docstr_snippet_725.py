class PropResourceLink(object):

    def __init__(self, clsname):
        self.clsname = clsname

    def __call__(self, resource=None):
        if resource is None:
            return self
        return resource