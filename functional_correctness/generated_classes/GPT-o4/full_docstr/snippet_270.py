class _Running:
    '''
    A generator of running, numerical IDs
    Should be enhanced by:
    - a member method for returning the size
    - a member iterator over the stored ids
    '''

    def __init__(self, orig_ids=False, warn=False):
        '''Constructor'''
        self._warn = warn
        self._id2num = {}
        self._next = 1
        if orig_ids:
            if isinstance(orig_ids, dict):
                for key, val in orig_ids.items():
                    if key in self._id2num and self._warn:
                        warnings.warn(f"Duplicate id {key} in orig_ids")
                    self._id2num[key] = val
                if self._id2num:
                    self._next = max(self._id2num.values()) + 1
            else:
                try:
                    for key in orig_ids:
                        if key in self._id2num and self._warn:
                            warnings.warn(f"Duplicate id {key} in orig_ids")
                        self._id2num[key] = self._next
                        self._next += 1
                except TypeError:
                    raise ValueError("orig_ids must be a dict or an iterable")

    def g(self, id):
        '''
        If the given id is known, the numerical representation is returned,
        otherwise a new running number is assigned to the id and returned
        '''
        if id in self._id2num:
            return self._id2num[id]
        num = self._next
        self._id2num[id] = num
        self._next += 1
        return num

    def k(self, id):
        '''
        Returns whether the given id is known.
        '''
        return id in self._id2num

    def d(self, id):
        '''
        Removed the element.
        '''
        if id in self._id2num:
            del self._id2num[id]
        else:
            if self._warn:
                warnings.warn(f"id {id} not found")

    def size(self):
        '''Return the number of stored ids.'''
        return len(self._id2num)

    def __len__(self):
        return len(self._id2num)

    def __iter__(self):
        return iter(self._id2num)