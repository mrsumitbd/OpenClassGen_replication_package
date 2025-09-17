class NamedKeyspace(object):
    '''
    A keyspace
    '''

    def __init__(self, name):
        self.name = name

    def table(self, name):
        '''
        returns a table descriptor with the given
        name that belongs to this keyspace
        '''
        return f"{self.name}.{name}"