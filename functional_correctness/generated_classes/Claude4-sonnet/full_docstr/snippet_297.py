class DaqmxDataReceiver(object):
    '''Receives raw scaler data for a DAQmx object and stores it in numpy
    arrays

    :ivar scaler_data: Dictionary mapping from scaler id to data for a scaler
    '''

    def __init__(self, obj, num_values, memmap_dir=None):
        '''Initialise data receiver for DAQmx backed by a numpy array

        :param obj: Object to store data for
        :param memmap_dir: Optional directory to store memory mmap files in.
        '''
        self.obj = obj
        self.num_values = num_values
        self.memmap_dir = memmap_dir if memmap_dir is not None else tempfile.gettempdir()
        self.scaler_data = {}
        self._data_arrays = {}
        self._current_indices = {}

    def append_scaler_data(self, scale_id, new_data):
        '''Append new DAQmx scaler data read from a segment
        '''
        if scale_id not in self.scaler_data:
            # Initialize memory-mapped array for this scaler
            filename = os.path.join(self.memmap_dir, f"scaler_{scale_id}_{id(self.obj)}.dat")
            self._data_arrays[scale_id] = np.memmap(filename, dtype=np.float64, mode='w+', shape=(self.num_values,))
            self._current_indices[scale_id] = 0
            self.scaler_data[scale_id] = self._data_arrays[scale_id]
        
        new_data = np.asarray(new_data)
        current_idx = self._current_indices[scale_id]
        end_idx = min(current_idx + len(new_data), self.num_values)
        
        if current_idx < self.num_values:
            self._data_arrays[scale_id][current_idx:end_idx] = new_data[:end_idx-current_idx]
            self._current_indices[scale_id] = end_idx