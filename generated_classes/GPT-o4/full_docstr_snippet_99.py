class _Run(object):
    '''Represents a batch of write operations.
    '''
    def __init__(self, op_type):
        '''Initialize a new Run object.
        '''
        self.op_type = op_type
        self._original_indexes = []
        self._operations = []

    def index(self, idx):
        '''Get the original index of an operation in this run.

        :Parameters:
          - `idx`: The Run index that maps to the original index.
        '''
        return self._original_indexes[idx]

    def add(self, original_index, operation):
        '''Add an operation to this Run instance.

        :Parameters:
          - `original_index`: The original index of this operation
            within a larger bulk operation.
          - `operation`: The operation document.
        '''
        self._original_indexes.append(original_index)
        self._operations.append(operation)