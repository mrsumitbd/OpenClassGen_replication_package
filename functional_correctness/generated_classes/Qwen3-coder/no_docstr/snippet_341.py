class Package(object):
    def __init__(self, dir, source):
        self.dir = dir
        self.source = source

    @property
    def path(self):
        return os.path.join(self.dir, self.source)

    @property
    def deploy_packages(self):
        deploy_dir = os.path.join(self.dir, 'deploy')
        if os.path.exists(deploy_dir):
            return [f for f in os.listdir(deploy_dir) 
                   if os.path.isfile(os.path.join(deploy_dir, f))]
        return []

    @property
    def dependencies(self):
        deps_file = os.path.join(self.dir, 'dependencies.txt')
        if os.path.exists(deps_file):
            with open(deps_file, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        return []