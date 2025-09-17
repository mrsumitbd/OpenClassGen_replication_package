class Buffer(object):
    def __init__(self, keys, n=None):
        self.keys = keys
        self.n = n if n is not None else 1000
        self.data = {key: [] for key in keys}
        self.min_length = 0
    
    def __contains__(self, item):
        return item in self.keys
    
    def is_readable(self):
        return self.min_length > 0
    
    def is_writable(self, key):
        if key not in self.keys:
            return False
        return len(self.data[key]) < self.n
    
    def read(self):
        if not self.is_readable():
            return None
        result = {}
        for key in self.keys:
            result[key] = self.data[key].pop(0)
        self._update_min_length()
        return result
    
    def write(self, key, values):
        if key not in self.keys:
            return False
        if not isinstance(values, list):
            values = [values]
        for value in values:
            if len(self.data[key]) < self.n:
                self.data[key].append(value)
            else:
                return False
        self._update_min_length()
        return True
    
    def _update_min_length(self):
        self.min_length = min(len(self.data[key]) for key in self.keys)