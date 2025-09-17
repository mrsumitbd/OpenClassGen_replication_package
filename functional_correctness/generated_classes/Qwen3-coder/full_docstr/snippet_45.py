class MorphLoader:
    '''Caching morphology loader.

    Arguments:
        directory: path to directory with morphology files
        file_ext: file extension to look for (if not set, will pick any of .swc|.h5|.asc)
        cache_size: size of LRU cache (if not set, no caching done)
    '''

    def __init__(self, directory, file_ext=None, cache_size=None):
        '''Initialize a MorphLoader object.'''
        self.directory = directory
        self.file_ext = file_ext
        self.cache_size = cache_size
        
        if cache_size is not None:
            self._cached_get = lru_cache(maxsize=cache_size)(self._load_morphology)
        else:
            self._cached_get = self._load_morphology

    def _filepath(self, name):
        '''File path to `name` morphology file.'''
        if self.file_ext is not None:
            return os.path.join(self.directory, f"{name}{self.file_ext}")
        
        # Check for supported extensions in order
        for ext in ['.swc', '.h5', '.asc']:
            filepath = os.path.join(self.directory, f"{name}{ext}")
            if os.path.exists(filepath):
                return filepath
        
        # If no file found, return with default extension preference
        return os.path.join(self.directory, f"{name}.swc")

    def _load_morphology(self, name):
        '''Load morphology data from file.'''
        filepath = self._filepath(name)
        
        # Check if file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Morphology file not found: {filepath}")
        
        # Get file extension
        _, ext = os.path.splitext(filepath)
        
        # Load based on extension
        if ext == '.swc':
            return self._load_swc(filepath)
        elif ext == '.h5':
            return self._load_h5(filepath)
        elif ext == '.asc':
            return self._load_asc(filepath)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    def _load_swc(self, filepath):
        '''Load SWC format morphology data.'''
        # Placeholder implementation - in real usage this would parse SWC files
        with open(filepath, 'r') as f:
            data = f.read()
        return {'type': 'swc', 'data': data, 'filepath': filepath}

    def _load_h5(self, filepath):
        '''Load HDF5 format morphology data.'''
        # Placeholder implementation - in real usage this would parse HDF5 files
        return {'type': 'h5', 'filepath': filepath}

    def _load_asc(self, filepath):
        '''Load ASC format morphology data.'''
        # Placeholder implementation - in real usage this would parse ASC files
        with open(filepath, 'r') as f:
            data = f.read()
        return {'type': 'asc', 'data': data, 'filepath': filepath}

    def get(self, name):
        '''Get `name` morphology data.'''
        return self._cached_get(name)