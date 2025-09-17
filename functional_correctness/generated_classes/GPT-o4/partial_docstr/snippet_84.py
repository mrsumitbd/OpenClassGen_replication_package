class RenameImport(object):
    '''
    A class for import hooks mapping Py3 module names etc. to the Py2 equivalents.
    '''

    def __init__(self, old_to_new):
        '''
        Pass in a dictionary-like object mapping from old names to new
        names. E.g. {'ConfigParser': 'configparser', 'cPickle': 'pickle'}
        '''
        self.old_to_new = dict(old_to_new)
        # sort keys by length so that longer (more specific) names match first
        self._keys = sorted(self.old_to_new, key=len, reverse=True)

    def find_module(self, fullname, path=None):
        for old in self._keys:
            if fullname == old or fullname.startswith(old + '.'):
                return self
        return None

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        for old in self._keys:
            if fullname == old or fullname.startswith(old + '.'):
                new = self.old_to_new[old]
                rest = fullname[len(old):]  # includes leading dot if submodule
                newname = new + rest
                break
        else:
            raise ImportError(fullname)

        module = self._find_and_load_module(newname)
        module.__name__ = fullname
        sys.modules[fullname] = module
        return module

    def _find_and_load_module(self, name, path=None):
        return importlib.import_module(name)