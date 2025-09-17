class RenameImport(object):
    '''
    A class for import hooks mapping Py3 module names etc. to the Py2 equivalents.
    '''

    def __init__(self, old_to_new):
        '''
        Pass in a dictionary-like object mapping from old names to new
        names. E.g. {'ConfigParser': 'configparser', 'cPickle': 'pickle'}
        '''
        self.old_to_new = old_to_new

    def find_module(self, fullname, path=None):
        if fullname in self.old_to_new:
            return self
        return None

    def load_module(self, name):
        if name in sys.modules:
            return sys.modules[name]
        
        new_name = self.old_to_new.get(name, name)
        module = self._find_and_load_module(new_name)
        
        sys.modules[name] = module
        return module

    def _find_and_load_module(self, name, path=None):
        '''
        Finds and loads it. But if there's a . in the name, handles it
        properly.
        '''
        if '.' in name:
            parts = name.split('.')
            parent_name = '.'.join(parts[:-1])
            parent = importlib.import_module(parent_name)
            return importlib.import_module(name)
        else:
            return importlib.import_module(name)