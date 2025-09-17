class _ExtMetaPath(object):
    def __init__(self):
        self._path_map = {}

    def find_module(self, fullname, submodule_path=None):
        path = self.try_find_module(fullname, submodule_path)
        if path:
            self._path_map[fullname] = path
            return self
        return None

    def try_find_module(self, fullname, submodule_path=None):
        name = fullname.rpartition('.')[-1]
        exts = importlib.machinery.EXTENSION_SUFFIXES
        search_paths = submodule_path if submodule_path is not None else sys.path
        for entry in search_paths:
            for ext in exts:
                fn = os.path.join(entry, name + ext)
                if os.path.isfile(fn):
                    return fn
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        path = self._path_map.get(fullname)
        if path is None:
            raise ImportError("Cannot load module %s" % fullname)
        loader = importlib.machinery.ExtensionFileLoader(fullname, path)
        spec = importlib.machinery.ModuleSpec(fullname, loader, origin=path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[fullname] = module
        loader.exec_module(module)
        return module