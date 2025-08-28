class NamedKeyspace(object):
    '''
    A keyspace
    '''

    def __init__(self, name):
        self.name = name
        self._tables = {}

    def table(self, name):
        '''
        returns a table descriptor with the given
        name that belongs to this keyspace
        '''
        if name not in self._tables:
            self._tables[name] = NamedTable(name, self)
        return self._tables[name]