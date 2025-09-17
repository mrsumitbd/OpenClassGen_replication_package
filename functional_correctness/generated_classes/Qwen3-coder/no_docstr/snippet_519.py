class ProjectDependencies:
    def __init__(self, pyproject_toml, pyenv_build):
        self.pyproject_toml = pyproject_toml
        self.pyenv_build = pyenv_build
        self.dependencies = {}
        self.dev_dependencies = {}
        self.optional_dependencies = {}

    def load(self):
        import toml
        import os
        
        # Load pyproject.toml
        if os.path.exists(self.pyproject_toml):
            with open(self.pyproject_toml, 'r') as f:
                config = toml.load(f)
            
            # Extract dependencies
            project_config = config.get('project', {})
            
            # Main dependencies
            self.dependencies = project_config.get('dependencies', {})
            
            # Development dependencies
            self.dev_dependencies = config.get('tool', {}).get('pytest', {}).get('dev-dependencies', {})
            
            # Optional dependencies
            self.optional_dependencies = project_config.get('optional-dependencies', {})
        
        # Load pyenv build information if available
        if os.path.exists(self.pyenv_build):
            with open(self.pyenv_build, 'r') as f:
                # Parse pyenv build file if needed
                pass