class Application(object):
    def __init__(self, path):
        self.path = path
        self.data = {}

    def run(self):
        # Simulate running the application
        print(f"Running application from path: {self.path}")
        return True

    def ids(self, file):
        # Return identifiers from the file
        if file not in self.data:
            self.data[file] = []
        return self.data[file]