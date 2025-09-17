class InstallationResult(object):

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"InstallationResult(name='{self.name}')"