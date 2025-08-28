class TempDir:
    def __init__(self):
        self._temp_dir = None
        self._is_open = False

    def open(self):
        if not self._is_open:
            self._temp_dir = tempfile.mkdtemp()
            self._is_open = True
        return self._temp_dir

    def close(self):
        if self._is_open and self._temp_dir:
            shutil.rmtree(self._temp_dir)
            self._temp_dir = None
            self._is_open = False