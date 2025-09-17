class TempDir:
    def __init__(self):
        self.path = None

    def open(self):
        if self.path is not None:
            raise RuntimeError("TempDir is already open")
        self.path = tempfile.mkdtemp()
        return self.path

    def close(self):
        if self.path is None:
            return
        shutil.rmtree(self.path, ignore_errors=True)
        self.path = None

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()