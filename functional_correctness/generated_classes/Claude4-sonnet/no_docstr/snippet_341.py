class Package(object):

    def __init__(self, dir, source):
        self.dir = dir
        self.source = source
        self._deploy_packages = None
        self._dependencies = None

    @property
    def path(self):
        return os.path.join(self.source, self.dir)

    @property
    def deploy_packages(self):
        if self._deploy_packages is None:
            package_json_path = os.path.join(self.path, 'package.json')
            if os.path.exists(package_json_path):
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    self._deploy_packages = package_data.get('deployPackages', [])
            else:
                self._deploy_packages = []
        return self._deploy_packages

    @property
    def dependencies(self):
        if self._dependencies is None:
            package_json_path = os.path.join(self.path, 'package.json')
            if os.path.exists(package_json_path):
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                    deps = package_data.get('dependencies', {})
                    dev_deps = package_data.get('devDependencies', {})
                    self._dependencies = list(set(list(deps.keys()) + list(dev_deps.keys())))
            else:
                self._dependencies = []
        return self._dependencies