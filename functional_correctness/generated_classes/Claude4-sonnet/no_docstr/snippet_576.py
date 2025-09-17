class Member:
    def __init__(self, hunk):
        self.hunk = hunk
        self.name = hunk.get('name', '')
        self.type = hunk.get('type', '')
        self.mode = hunk.get('mode', 0)
        self.size = hunk.get('size', 0)

    def isfile(self):
        return self.type == 'file' or (hasattr(self, 'mode') and self.mode & 0o170000 == 0o100000)

    def isdir(self):
        return self.type == 'dir' or (hasattr(self, 'mode') and self.mode & 0o170000 == 0o040000)