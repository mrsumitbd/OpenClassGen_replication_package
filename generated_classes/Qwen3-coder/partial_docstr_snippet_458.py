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
        self.size = 0
        
        if byte_data is not None:
            self._parse_byte_data(byte_data)
        elif file_obj is not None:
            self._parse_file(file_obj)

    def _parse_byte_data(self, byte_data):
        '''Extract the values from byte string.'''
        # Assuming the size is stored as a 4-byte little-endian integer at the beginning
        if len(byte_data) >= 4:
            import struct
            self.size = struct.unpack('<I', byte_data[:4])[0]

    def _parse_file(self, file_obj):
        '''Directly read from file handler.

        Note:
          This will move the file pointer.

        '''
        # Read 4 bytes for the size field
        byte_data = file_obj.read(4)
        if len(byte_data) == 4:
            import struct
            self.size = struct.unpack('<I', byte_data)[0]

    def __repr__(self):
        return f"DAQHeader(size={self.size})"