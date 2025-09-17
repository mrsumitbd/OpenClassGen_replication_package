class PlpReader(object):
    '''Partially length prefixed reader

    Spec: http://msdn.microsoft.com/en-us/library/dd340469.aspx
    '''

    def __init__(self, r):
        '''
        :param r: An instance of :class:`_TdsReader`
        '''
        self._r = r
        self._is_null = None
        self._is_unknown_len = None
        self._size = None
        self._finished = False

    def is_null(self):
        '''
        :return: True if stored value is NULL
        '''
        if self._is_null is None:
            self._read_header()
        return self._is_null

    def is_unknown_len(self):
        '''
        :return: True if total size is unknown upfront
        '''
        if self._is_unknown_len is None:
            self._read_header()
        return self._is_unknown_len

    def size(self):
        '''
        :return: Total size in bytes if is_uknown_len and is_null are both False
        '''
        if self._size is None:
            self._read_header()
        return self._size

    def chunks(self):
        '''Generates chunks from stream, each chunk is an instace of bytes.'''
        if self.is_null():
            return
        
        if self.is_unknown_len():
            while not self._finished:
                chunk_len = self._r.read_uint32()
                if chunk_len == 0:
                    self._finished = True
                    break
                yield self._r.read(chunk_len)
        else:
            remaining = self._size
            while remaining > 0:
                chunk_len = min(remaining, 0x7FFFFFFF)  # Max chunk size
                yield self._r.read(chunk_len)
                remaining -= chunk_len

    def _read_header(self):
        '''Read the PLP header to determine null status, unknown length, and size'''
        length = self._r.read_uint64()
        if length == 0xFFFFFFFFFFFFFFFF:
            self._is_null = True
            self._is_unknown_len = False
            self._size = 0
        elif length == 0xFFFFFFFFFFFFFFFE:
            self._is_null = False
            self._is_unknown_len = True
            self._size = 0
        else:
            self._is_null = False
            self._is_unknown_len = False
            self._size = length