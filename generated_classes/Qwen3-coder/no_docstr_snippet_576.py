class Member:
    def __init__(self, hunk):
        self.hunk = hunk

    def isfile(self):
        return not self.isdir()

    def isdir(self):
        return hasattr(self.hunk, 'isdir') and self.hunk.isdir()