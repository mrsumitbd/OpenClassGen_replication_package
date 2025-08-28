class Enum:
    '''Map values to specific strings.'''

    def __init__(self, *args, **kwargs):
        '''Initialize the mapping.'''
        self._name_to_val = {}
        self._val_to_name = {}
        next_val = 0
        # assign positional args
        for name in args:
            if not isinstance(name, str):
                raise TypeError('Enum names must be strings')
            if name in self._name_to_val:
                raise ValueError(f'Duplicate enum name: {name}')
            self._name_to_val[name] = next_val
            self._val_to_name[next_val] = name
            next_val += 1
        # assign keyword args
        for name, val in kwargs.items():
            if not isinstance(name, str):
                raise TypeError('Enum names must be strings')
            if not isinstance(val, int):
                raise TypeError('Enum values must be integers')
            if name in self._name_to_val:
                # remove old mapping
                old_val = self._name_to_val[name]
                del self._val_to_name[old_val]
            if val in self._val_to_name:
                raise ValueError(f'Duplicate enum value: {val}')
            self._name_to_val[name] = val
            self._val_to_name[val] = name
        # set attributes
        for name, val in self._name_to_val.items():
            setattr(self, name, val)

    def __call__(self, val):
        '''Map an integer to the string representation.'''
        try:
            return self._val_to_name[val]
        except KeyError:
            raise KeyError(f'Invalid enum value: {val}')