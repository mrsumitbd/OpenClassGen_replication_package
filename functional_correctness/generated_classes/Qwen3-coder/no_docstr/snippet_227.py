class InstallationResult(object):
    def __init__(self, name):
        self.name = name
        self.success = False
        self.message = ""
        self.details = {}

    def __repr__(self):
        return f"InstallationResult(name='{self.name}', success={self.success}, message='{self.message}')"