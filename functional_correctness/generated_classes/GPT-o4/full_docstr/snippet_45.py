class MorphLoader:
    '''Caching morphology loader.

    Arguments:
        directory: path to directory with morphology files
        file_ext: file extension to look for (if not set, will pick any of .swc|.h5|.asc)
        cache_size: size of LRU cache (if not set, no caching done)
    '''

    def __init__(self, directory, file_ext=None, cache_size=None):
        '''Initialize a MorphLoader object.'''
        self.directory = Path(directory)
        if file_ext:
            file_ext = file_ext if file_ext.startswith('.') else f'.{file_ext}'
        self.file_ext = file_ext
        self.cache_size = cache_size
        if cache_size:
            self._cache = OrderedDict()

    def _filepath(self, name):
        '''File path to `name` morphology file.'''
        if self.file_ext:
            candidate = self.directory / f"{name}{self.file_ext}"
            if candidate.is_file():
                return candidate
            else:
                raise FileNotFoundError(f"No file {candidate}")
        else:
            for ext in ('.swc', '.h5', '.asc'):
                candidate = self.directory / f"{name}{ext}"
                if candidate.is_file():
                    return candidate
            raise FileNotFoundError(f"No morphology file for {name} in {self.directory}")

    def get(self, name):
        '''Get `name` morphology data.'''
        if self.cache_size:
            if name in self._cache:
                self._cache.move_to_end(name)
                return self._cache[name]
        path = self._filepath(name)
        data = path.read_bytes()
        if self.cache_size:
            self._cache[name] = data
            if len(self._cache) > self.cache_size:
                self._cache.popitem(last=False)
        return data