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
        return self.try_find_module(fullname, submodule_path)

    def try_find_module(self, fullname, submodule_path=None):
        # Convert module name to file path format
        module_path = fullname.replace('.', os.sep)
        
        # Determine search paths
        if submodule_path is not None:
            search_paths = submodule_path
        else:
            search_paths = sys.path
        
        # Look for .so files (compiled extensions)
        for path in search_paths:
            # Check for direct module.so
            so_file = os.path.join(path, module_path + '.so')
            if os.path.exists(so_file):
                return self
            
            # Check for module/__init__.so (package format)
            init_so_file = os.path.join(path, module_path, '__init__.so')
            if os.path.exists(init_so_file):
                return self
        
        return None

    def load_module(self, fullname):
        # Check if module is already loaded
        if fullname in sys.modules:
            return sys.modules[fullname]
        
        # Convert module name to file path format
        module_path = fullname.replace('.', os.sep)
        
        # Try to find the module file
        module_file = None
        is_package = False
        
        for path in sys.path:
            # Check for direct module.so
            so_file = os.path.join(path, module_path + '.so')
            if os.path.exists(so_file):
                module_file = so_file
                break
            
            # Check for module/__init__.so (package format)
            init_so_file = os.path.join(path, module_path, '__init__.so')
            if os.path.exists(init_so_file):
                module_file = init_so_file
                is_package = True
                break
        
        if module_file is None:
            raise ImportError(f"No module named '{fullname}'")
        
        # Create module spec and module
        spec = importlib.util.spec_from_file_location(fullname, module_file)
        if spec is None:
            raise ImportError(f"Cannot load spec for module '{fullname}'")
        
        module = importlib.util.module_from_spec(spec)
        
        # Set module attributes
        module.__file__ = module_file
        module.__loader__ = self
        if is_package:
            module.__path__ = [os.path.dirname(module_file)]
            module.__package__ = fullname
        else:
            module.__package__ = fullname.rpartition('.')[0] if '.' in fullname else None
        
        # Add to sys.modules before executing
        sys.modules[fullname] = module
        
        # Execute the module
        try:
            spec.loader.exec_module(module)
        except Exception:
            # If execution fails, remove from sys.modules
            del sys.modules[fullname]
            raise
        
        return module