class Enum:
    '''Map values to specific strings.'''

    def __init__(self, *args, **kwargs):
        '''Initialize the mapping.'''
        self._mapping = {}
        
        # Handle positional arguments (list of strings)
        for i, value in enumerate(args):
            self._mapping[i] = value
        
        # Handle keyword arguments (explicit key-value pairs)
        for key, value in kwargs.items():
            if isinstance(key, str) and key.isdigit():
                self._mapping[int(key)] = value
            else:
                # For non-numeric string keys, we need to handle them appropriately
                # This assumes the key should be converted to its hash or some numeric representation
                self._mapping[hash(key) % 1000] = value

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        return self._mapping.get(val, str(val))