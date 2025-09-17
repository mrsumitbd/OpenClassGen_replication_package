class DAQHeader(object):
    '''Wrapper for the JDAQHeader binary format.

    Parameters
    ----------
    byte_data : bytes (optional)
        The binary file, where the file pointer is at the beginning of the header.
    file_obj : file (optional)
        The binary file, where the file pointer is at the beginning of the header.

    Attributes
    ----------
    size : int
        The size of the original DAQ byte representation.
    '''

    def __init__(self, byte_data=None, file_obj=None):
        if (byte_data is None and file_obj is None) or (byte_data is not None and file_obj is not None):
            raise ValueError("Provide exactly one of byte_data or file_obj")
        if byte_data is not None:
            self._parse_byte_data(byte_data)
        else:
            self._parse_file(file_obj)

    def _parse_byte_data(self, byte_data):
        '''Extract the values from byte string.'''
        # Expect first 4 bytes to encode the total header size as a little‐endian uint32
        if len(byte_data) < 4:
            raise ValueError("byte_data too short to contain size field")
        size_field = struct.unpack('<I', byte_data[:4])[0]
        self.size = size_field
        # Store raw header bytes if you like; at minimum we keep size
        self._raw = byte_data

    def _parse_file(self, file_obj):
        '''Directly read from file handler.

        Note:
          This will move the file pointer.
        '''
        # Read the size field first
        size_bytes = file_obj.read(4)
        if len(size_bytes) < 4:
            raise EOFError("Could not read header size from file")
        size_field = struct.unpack('<I', size_bytes)[0]
        self.size = size_field
        # Now read the rest of the header
        remaining = size_field - 4
        if remaining < 0:
            raise ValueError("Invalid header size")
        data_bytes = file_obj.read(remaining)
        if len(data_bytes) < remaining:
            raise EOFError("File ended before reading full header")
        self._raw = size_bytes + data_bytes

    def __repr__(self):
        return f"<{self.__class__.__name__} size={self.size}>"