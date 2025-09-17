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
        self.memmap_dir = memmap_dir
        self.scaler_data = {}
        self._counts = {}
        if self.memmap_dir is not None:
            os.makedirs(self.memmap_dir, exist_ok=True)

    def append_scaler_data(self, scale_id, new_data):
        '''Append new DAQmx scaler data read from a segment'''
        data = np.atleast_1d(new_data).astype(np.int64)
        n = data.shape[0]
        if scale_id not in self.scaler_data:
            if self.memmap_dir:
                fname = os.path.join(
                    self.memmap_dir,
                    f"daqmx_obj_{id(self.obj)}_scaler_{scale_id}.dat"
                )
                arr = np.memmap(fname, dtype=np.int64,
                                mode="w+", shape=(self.num_values,))
            else:
                arr = np.zeros(self.num_values, dtype=np.int64)
            self.scaler_data[scale_id] = arr
            self._counts[scale_id] = 0
        start = self._counts[scale_id]
        end = start + n
        if end > self.num_values:
            raise ValueError(
                f"Appending {n} values exceeds capacity of {self.num_values}"
            )
        self.scaler_data[scale_id][start:end] = data
        self._counts[scale_id] = end