class _ExtMetaPath(object):
    '''
    This is a magic metapath searcher. To understand how this works,
    See the PEP 302 document. Essentially this class is inserted into
    the sys.meta_path list. This class must implement find_module()
    and load_module(). After which, this class is called first when any
    particular module import was requested, allowing this to essentially
    'override' the default import behaviors.
    '''

    def find_module(self, fullname, submodule_path=None):
        '''
        We have to see if fullname refers to a module we can import.
        Some care is needed here because:

        import xxx   # tries to load xxx.so from any of the python import paths
        import aaa.bbb.xxx # tries to load aaa/bbb/xxx.so from any of the python import paths
        '''
        result = self.try_find_module(fullname, submodule_path)
        if result:
            return self
        return None

    def try_find_module(self, fullname, submodule_path=None):
        if fullname in sys.modules:
            return sys.modules[fullname]
        
        # Convert module name to file path
        parts = fullname.split('.')
        filename = parts[-1] + '.so'
        
        # Search in sys.path
        search_paths = submodule_path if submodule_path else sys.path
        
        for path in search_paths:
            if not path:
                continue
                
            # For nested modules like aaa.bbb.xxx, construct the full path
            if len(parts) > 1:
                nested_path = os.path.join(path, *parts[:-1])
                full_path = os.path.join(nested_path, filename)
            else:
                full_path = os.path.join(path, filename)
            
            if os.path.exists(full_path):
                return full_path
        
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        
        module_path = self.try_find_module(fullname)
        if not module_path:
            raise ImportError(f"No module named '{fullname}'")
        
        # Create module spec and load
        spec = importlib.util.spec_from_file_location(fullname, module_path)
        if spec is None:
            raise ImportError(f"Could not load spec for '{fullname}'")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[fullname] = module
        
        try:
            spec.loader.exec_module(module)
        except Exception:
            if fullname in sys.modules:
                del sys.modules[fullname]
            raise
        
        return module