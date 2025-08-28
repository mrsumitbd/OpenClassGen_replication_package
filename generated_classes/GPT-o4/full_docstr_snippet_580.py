class PlpReader(object):
    '''Partially length prefixed reader

    Spec: http://msdn.microsoft.com/en-us/library/dd340469.aspx
    '''

    NULL_LEN = 0xFFFFFFFFFFFFFFFE
    UNKNOWN_LEN = 0xFFFFFFFFFFFFFFFF

    def __init__(self, r):
        '''
            :param r: An instance of :class:`_TdsReader`
        '''
        self._r = r
        raw = self._r.read(8)
        if len(raw) < 8:
            raise EOFError("Unable to read PLP total length")
        self._total_length = struct.unpack('<Q', raw)[0]

    def is_null(self):
        '''
            :return: True if stored value is NULL
        '''
        return self._total_length == self.NULL_LEN

    def is_unknown_len(self):
        '''
            :return: True if total size is unknown upfront
        '''
        return self._total_length == self.UNKNOWN_LEN

    def size(self):
        '''
            :return: Total size in bytes if is_unknown_len and is_null are both False
        '''
        if self.is_null():
            raise ValueError("Value is NULL")
        if self.is_unknown_len():
            raise ValueError("Total size is unknown")
        return self._total_length

    def chunks(self):
        '''Generates chunks from stream, each chunk is an instance of bytes.'''
        if self.is_null():
            return
        while True:
            raw = self._r.read(4)
            if len(raw) < 4:
                raise EOFError("Unable to read PLP chunk length")
            chunk_len = struct.unpack('<I', raw)[0]
            if chunk_len == 0:
                break
            data = self._r.read(chunk_len)
            if len(data) < chunk_len:
                raise EOFError("Unable to read full PLP chunk")
            yield data