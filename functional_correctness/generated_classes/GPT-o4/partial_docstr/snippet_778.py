class Path(object):
    '''
    This class represents a path in a JSON value
    '''

    @staticmethod
    def rootPath():
        '''Returns the root path's string representation'''
        return '$'

    def __init__(self, path):
        '''
        Make a new path based on the string representation in `path`
        '''
        if not isinstance(path, str):
            raise TypeError("Path must be a string")
        if path == '':
            raise ValueError("Path string cannot be empty")
        if path != '$' and not path.startswith('$.'):
            raise ValueError("Path must start with '$' or '$.'")
        self._raw = path
        self.segments = []
        if path == '$':
            return
        # parse after the leading '$'
        i = 1
        n = len(path)
        while i < n:
            c = path[i]
            if c == '.':
                m = re.match(r'\.([A-Za-z_][A-Za-z0-9_]*)', path[i:])
                if not m:
                    raise ValueError(f"Invalid object key at position {i}")
                key = m.group(1)
                self.segments.append(key)
                i += m.end()
            elif c == '[':
                m = re.match(r'\[(\d+)\]', path[i:])
                if not m:
                    raise ValueError(f"Invalid array index at position {i}")
                idx = int(m.group(1))
                self.segments.append(idx)
                i += m.end()
            else:
                raise ValueError(f"Unexpected character '{c}' at position {i}")

    def __str__(self):
        return self._raw

    def __repr__(self):
        return f"Path('{self._raw}')"

    def __eq__(self, other):
        if not isinstance(other, Path):
            return False
        return self._raw == other._raw

    def __hash__(self):
        return hash(self._raw)