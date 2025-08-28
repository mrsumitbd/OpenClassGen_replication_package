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
        
    def append_scaler_data(self, scale_id, new_data):
        '''Append new DAQmx scaler data read from a segment
        '''
        if scale_id not in self.scaler_data:
            if self.memmap_dir is not None:
                # Create memory mapped array
                mmap_file = os.path.join(self.memmap_dir, f'scaler_{scale_id}.npy')
                self.scaler_data[scale_id] = np.memmap(mmap_file, dtype=new_data.dtype, mode='w+', shape=(self.num_values,))
                self.scaler_data[scale_id][:len(new_data)] = new_data
            else:
                # Create regular numpy array
                self.scaler_data[scale_id] = np.zeros(self.num_values, dtype=new_data.dtype)
                self.scaler_data[scale_id][:len(new_data)] = new_data
        else:
            # Append to existing data
            existing_data = self.scaler_data[scale_id]
            current_length = np.count_nonzero(existing_data) if existing_data.dtype != object else len([x for x in existing_data if x != 0])
            end_index = min(current_length + len(new_data), self.num_values)
            self.scaler_data[scale_id][current_length:end_index] = new_data[:end_index-current_length]