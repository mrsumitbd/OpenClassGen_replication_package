class Application(object):

    def __init__(self, path):
        self.path = path

    def run(self):
        if os.path.exists(self.path):
            subprocess.run([self.path])

    def ids(self, file):
        if os.path.exists(file):
            with open(file, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []