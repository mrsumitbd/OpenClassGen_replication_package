class _X509extlist(object):
    '''
    Represents list of certificate extensions. Really it keeps
    reference to certificate object
    '''

    def __init__(self, cert):
        '''
        Initialize from X509 object
        '''
        self.cert = cert

    def __len__(self):
        '''
        Returns number of extensions
        '''
        return self.cert.get_extension_count()

    def __getitem__(self, item):
        '''
        Returns extension by index, creating a copy
        '''
        if item < 0 or item >= len(self):
            raise IndexError("Extension index out of range")
        return self.cert.get_extension(item)

    def find(self, oid):
        '''
        Return list of extensions with given Oid
        '''
        result = []
        for i in range(len(self)):
            ext = self[i]
            if ext.get_short_name() == oid or str(ext.get_oid()) == oid:
                result.append(ext)
        return result

    def find_critical(self, crit=True):
        '''
        Return list of critical extensions (or list of non-cricital, if
        optional second argument is False
        '''
        result = []
        for i in range(len(self)):
            ext = self[i]
            if ext.get_critical() == crit:
                result.append(ext)
        return result