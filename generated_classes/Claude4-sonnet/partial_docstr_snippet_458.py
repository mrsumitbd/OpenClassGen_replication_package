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
        self.detector_id = 0
        self.run_id = 0
        self.time_slice = 0
        self.time_stamp = 0
        self.tick = 0
        self.overlays = 0
        self.trigger_counter = 0
        self.trigger_mask = 0
        self.data_type = 0
        
        if byte_data is not None:
            self._parse_byte_data(byte_data)
        elif file_obj is not None:
            self._parse_file(file_obj)

    def _parse_byte_data(self, byte_data):
        '''Extract the values from byte string.'''
        if len(byte_data) < 40:
            raise ValueError("Insufficient byte data for DAQ header")
        
        values = struct.unpack('<10I', byte_data[:40])
        self.size = values[0]
        self.detector_id = values[1]
        self.run_id = values[2]
        self.time_slice = values[3]
        self.time_stamp = values[4]
        self.tick = values[5]
        self.overlays = values[6]
        self.trigger_counter = values[7]
        self.trigger_mask = values[8]
        self.data_type = values[9]

    def _parse_file(self, file_obj):
        '''Directly read from file handler.

        Note:
          This will move the file pointer.

        '''
        byte_data = file_obj.read(40)
        if len(byte_data) < 40:
            raise ValueError("Insufficient data in file for DAQ header")
        self._parse_byte_data(byte_data)

    def __repr__(self):
        return (f"DAQHeader(size={self.size}, detector_id={self.detector_id}, "
                f"run_id={self.run_id}, time_slice={self.time_slice}, "
                f"time_stamp={self.time_stamp}, tick={self.tick}, "
                f"overlays={self.overlays}, trigger_counter={self.trigger_counter}, "
                f"trigger_mask={self.trigger_mask}, data_type={self.data_type})")