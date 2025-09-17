class Enum:
    '''Map values to specific strings.'''

    def __init__(self, *args, **kwargs):
        '''Initialize the mapping.'''
        self._mapping = {}
        
        # Handle positional arguments
        for i, arg in enumerate(args):
            self._mapping[i] = arg
            
        # Handle keyword arguments
        for key, value in kwargs.items():
            if isinstance(key, int):
                self._mapping[key] = value
            else:
                # If key is not an integer, use its position
                self._mapping[len(self._mapping)] = key

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        return self._mapping.get(val, None)