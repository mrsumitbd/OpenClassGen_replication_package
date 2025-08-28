class _Running:
    '''
    A generator of running, numerical IDs
    Should be enhanced by:
    - a member method for returning the size
    - a member iterator over the stored ids
    '''

    def __init__(self, orig_ids=False, warn=False):
        '''Contructor'''
        self.orig_ids = orig_ids
        self.warn = warn
        self.id_to_num = {}
        self.num_to_id = {}
        self.next_num = 0

    def g(self, id):
        '''
        If the given id is known, the numerical representation is returned,
        otherwise a new running number is assigned to the id and returned'''
        if id in self.id_to_num:
            return self.id_to_num[id]
        else:
            num = self.next_num
            self.id_to_num[id] = num
            self.num_to_id[num] = id
            self.next_num += 1
            return num

    def k(self, id):
        '''
        Returns whether the given id is known.'''
        return id in self.id_to_num

    def d(self, id):
        '''
        Removed the element.'''
        if id in self.id_to_num:
            num = self.id_to_num[id]
            del self.id_to_num[id]
            del self.num_to_id[num]

    def size(self):
        return len(self.id_to_num)

    def __iter__(self):
        return iter(self.id_to_num.keys())