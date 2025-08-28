class ProjectDependencies:
    def __init__(self, pyproject_toml, pyenv_build):
        self.pyproject_toml = Path(pyproject_toml)
        self.pyenv_build = pyenv_build

    def load(self):
        content = self.pyproject_toml.read_text(encoding="utf-8")
        data = toml.loads(content)
        poetry = data.get("tool", {}).get("poetry", {})
        main_deps = poetry.get("dependencies", {})
        dev_deps = poetry.get("dev-dependencies", {})

        built = {
            "dependencies": [],
            "dev-dependencies": []
        }

        for name, spec in main_deps.items():
            if name.lower() == "python":
                continue
            built_dep = self.pyenv_build.build(name, spec, dev=False)
            built["dependencies"].append(built_dep)

        for name, spec in dev_deps.items():
            built_dep = self.pyenv_build.build(name, spec, dev=True)
            built["dev-dependencies"].append(built_dep)

        return built