class _X509extlist(object):
    '''
    Represents list of certificate extensions. Really it keeps
    reference to certificate object
    '''

    def __init__(self, cert):
        '''
        Initialize from X509 object
        '''
        self._cert = cert

    def __len__(self):
        '''
        Returns number of extensions
        '''
        if hasattr(self._cert, 'get_extension_count'):
            return self._cert.get_extension_count()
        # fallback if get_extensions() is provided
        exts = getattr(self._cert, 'get_extensions', None)
        if exts:
            return len(self._cert.get_extensions())
        raise AttributeError("Certificate object has no extensions interface")

    def __getitem__(self, item):
        '''
        Returns extension by index, creating a copy
        '''
        n = len(self)
        if isinstance(item, slice):
            start, stop, step = item.indices(n)
            return [self[i] for i in range(start, stop, step)]
        # handle negative indices
        if item < 0:
            item = n + item
        if item < 0 or item >= n:
            raise IndexError("Extension index out of range")
        if hasattr(self._cert, 'get_extension'):
            ext = self._cert.get_extension(item)
        else:
            exts = self._cert.get_extensions()
            ext = exts[item]
        return copy.copy(ext)

    def find(self, oid):
        '''
        Return list of extensions with given Oid
        '''
        matches = []
        for i in range(len(self)):
            ext = self._cert.get_extension(i) if hasattr(self._cert, 'get_extension') else self._cert.get_extensions()[i]
            obj = ext.get_object()
            short = obj.get_short_name()
            longn = obj.get_long_name()
            if oid == short or oid == longn or (isinstance(oid, str) and (oid == short.decode() or oid == longn.decode())):
                matches.append(copy.copy(ext))
        return matches

    def find_critical(self, crit=True):
        '''
        Return list of critical extensions (or list of non-cricital, if
        optional second argument is False
        '''
        matches = []
        for i in range(len(self)):
            ext = self._cert.get_extension(i) if hasattr(self._cert, 'get_extension') else self._cert.get_extensions()[i]
            if ext.get_critical() == bool(crit):
                matches.append(copy.copy(ext))
        return matches