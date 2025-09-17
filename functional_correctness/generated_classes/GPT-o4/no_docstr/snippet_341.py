class Package(object):

    def __init__(self, dir, source):
        self.dir = dir
        self.source = source

    @property
    def path(self):
        return os.path.abspath(os.path.join(self.dir, self.source))

    @property
    def deploy_packages(self):
        pkgs = []
        base = self.path
        for root, dirs, files in os.walk(base):
            if '__init__.py' in files:
                rel = os.path.relpath(root, base)
                if rel == '.':
                    name = os.path.basename(base)
                else:
                    name = rel.replace(os.sep, '.')
                pkgs.append(name)
        return sorted(pkgs)

    @property
    def dependencies(self):
        req_file = os.path.join(self.path, 'requirements.txt')
        if not os.path.isfile(req_file):
            return []
        deps = []
        with open(req_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    deps.append(line)
        return deps