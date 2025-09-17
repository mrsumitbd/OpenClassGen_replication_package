class Application(object):

    def __init__(self, path):
        self.path = path

    def run(self):
        files = []
        if os.path.isdir(self.path):
            for root, _, filenames in os.walk(self.path):
                for fn in filenames:
                    files.append(os.path.join(root, fn))
        elif os.path.isfile(self.path):
            files.append(self.path)

        for f in files:
            found = self.ids(f)
            if found:
                print(f)
                for i in sorted(found):
                    print(i)

    def ids(self, file):
        results = set()
        pattern = re.compile(r'\b\d+\b')
        try:
            with open(file, 'r') as fp:
                for line in fp:
                    for m in pattern.findall(line):
                        results.add(int(m))
        except (IOError, OSError):
            pass
        return results