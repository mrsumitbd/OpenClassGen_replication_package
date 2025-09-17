class TempDir:
    def __init__(self):
        self.path = None

    def open(self):
        self.path = tempfile.mkdtemp()
        return self.path

    def close(self):
        if self.path and os.path.exists(self.path):
            shutil.rmtree(self.path)
            self.path = None