class Member:
    def __init__(self, hunk):
        self._path = Path(hunk)

    def isfile(self):
        return self._path.is_file()

    def isdir(self):
        return self._path.is_dir()