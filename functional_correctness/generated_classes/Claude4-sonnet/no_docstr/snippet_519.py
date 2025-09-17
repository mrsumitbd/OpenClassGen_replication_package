class ProjectDependencies:
    def __init__(self, pyproject_toml, pyenv_build):
        self.pyproject_toml = pyproject_toml
        self.pyenv_build = pyenv_build
        self.dependencies = {}
        self.dev_dependencies = {}
        self.build_dependencies = {}
        self.python_version = None

    def load(self):
        if os.path.exists(self.pyproject_toml):
            with open(self.pyproject_toml, 'r') as f:
                data = toml.load(f)
            
            # Load project dependencies
            if 'project' in data and 'dependencies' in data['project']:
                self.dependencies = {dep.split('==')[0] if '==' in dep else dep.split('>=')[0] if '>=' in dep else dep.split('~=')[0] if '~=' in dep else dep: dep for dep in data['project']['dependencies']}
            
            # Load optional dependencies (dev dependencies)
            if 'project' in data and 'optional-dependencies' in data['project']:
                for group, deps in data['project']['optional-dependencies'].items():
                    self.dev_dependencies[group] = {dep.split('==')[0] if '==' in dep else dep.split('>=')[0] if '>=' in dep else dep.split('~=')[0] if '~=' in dep else dep: dep for dep in deps}
            
            # Load build system dependencies
            if 'build-system' in data and 'requires' in data['build-system']:
                self.build_dependencies = {dep.split('==')[0] if '==' in dep else dep.split('>=')[0] if '>=' in dep else dep.split('~=')[0] if '~=' in dep else dep: dep for dep in data['build-system']['requires']}
            
            # Load Python version requirement
            if 'project' in data and 'requires-python' in data['project']:
                self.python_version = data['project']['requires-python']
        
        if os.path.exists(self.pyenv_build):
            with open(self.pyenv_build, 'r') as f:
                content = f.read().strip()
                if content:
                    self.python_version = content