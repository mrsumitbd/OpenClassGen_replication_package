class PlpReader(object):
    '''Partially length prefixed reader

    Spec: http://msdn.microsoft.com/en-us/library/dd340469.aspx
    '''

    def __init__(self, r):
        '''
        :param r: An instance of :class:`_TdsReader`
        '''
        self._reader = r
        self._size = r.get_uint8()
        
        if self._size == 0xFFFFFFFFFFFFFFFF:
            # NULL value
            self._is_null = True
            self._is_unknown_len = False
            self._total_size = 0
        elif self._size == 0xFFFFFFFFFFFFFFFE:
            # Unknown length
            self._is_null = False
            self._is_unknown_len = True
            self._total_size = 0
        else:
            # Known length
            self._is_null = False
            self._is_unknown_len = False
            self._total_size = self._size

    def is_null(self):
        '''
        :return: True if stored value is NULL
        '''
        return self._is_null

    def is_unknown_len(self):
        '''
        :return: True if total size is unknown upfront
        '''
        return self._is_unknown_len

    def size(self):
        '''
        :return: Total size in bytes if is_uknown_len and is_null are both False
        '''
        if self._is_unknown_len or self._is_null:
            return None
        return self._total_size

    def chunks(self):
        '''Generates chunks from stream, each chunk is an instace of bytes.'''
        if self._is_null:
            return
            
        if self._is_unknown_len:
            while True:
                chunk_len = self._reader.get_uint4()
                if chunk_len == 0:
                    break
                yield self._reader.read(chunk_len)
        else:
            remaining = self._total_size
            while remaining > 0:
                chunk_len = self._reader.get_uint4()
                if chunk_len == 0:
                    break
                chunk_data = self._reader.read(chunk_len)
                remaining -= chunk_len
                yield chunk_data