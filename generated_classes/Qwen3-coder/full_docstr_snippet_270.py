class _Running:
    '''
    A generator of running, numerical IDs
    Should be enhanced by:
    - a member method for returning the size
    - a member iterator over the stored ids
    '''

    def __init__(self, orig_ids=False, warn=False):
        '''Constructor'''
        self._id_map = {}
        self._next_id = 0
        self._orig_ids = orig_ids
        self._warn = warn

    def g(self, id):
        '''
        If the given id is known, the numerical representation is returned,
        otherwise a new running number is assigned to the id and returned'''
        if id in self._id_map:
            return self._id_map[id]
        else:
            num_id = self._next_id
            self._id_map[id] = num_id
            self._next_id += 1
            return num_id

    def k(self, id):
        '''
        Returns whether the given id is known.'''
        return id in self._id_map

    def d(self, id):
        '''
        Removed the element.'''
        if id in self._id_map:
            del self._id_map[id]

    def size(self):
        '''Returns the number of stored ids'''
        return len(self._id_map)

    def __iter__(self):
        '''Iterator over the stored ids'''
        return iter(self._id_map)