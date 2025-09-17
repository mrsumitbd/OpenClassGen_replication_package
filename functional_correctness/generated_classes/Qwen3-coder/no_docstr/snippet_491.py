class Buffer(object):
    def __init__(self, keys, n=None):
        self.keys = keys
        self.n = n
        self.data = {key: [] for key in keys}
        self.read_positions = {key: 0 for key in keys}
    
    def __contains__(self, item):
        return item in self.keys
    
    def is_readable(self):
        for key in self.keys:
            if len(self.data[key]) > self.read_positions[key]:
                return True
        return False
    
    def is_writable(self, key):
        if key not in self.keys:
            return False
        if self.n is None:
            return True
        return len(self.data[key]) < self.n
    
    def read(self):
        result = {}
        for key in self.keys:
            if len(self.data[key]) > self.read_positions[key]:
                result[key] = self.data[key][self.read_positions[key]]
                self.read_positions[key] += 1
            else:
                result[key] = None
        return result
    
    def write(self, key, values):
        if key not in self.keys:
            return False
        if self.n is not None and len(self.data[key]) + len(values) > self.n:
            return False
        self.data[key].extend(values)
        return True