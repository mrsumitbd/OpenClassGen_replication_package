class InstallationResult(object):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"