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
            self._cached_load = lru_cache(maxsize=cache_size)(self._load_morphology)
        else:
            self._cached_load = self._load_morphology

    def _filepath(self, name):
        '''File path to `name` morphology file.'''
        if self.file_ext:
            return os.path.join(self.directory, f"{name}.{self.file_ext}")
        else:
            # Look for any of the supported extensions
            for ext in ['swc', 'h5', 'asc']:
                filepath = os.path.join(self.directory, f"{name}.{ext}")
                if os.path.exists(filepath):
                    return filepath
            # If no file found, return the first extension as default
            return os.path.join(self.directory, f"{name}.swc")

    def _load_morphology(self, filepath):
        '''Load morphology from file.'''
        return morphio.Morphology(filepath)

    def get(self, name):
        '''Get `name` morphology data.'''
        filepath = self._filepath(name)
        return self._cached_load(filepath)