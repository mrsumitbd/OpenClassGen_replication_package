class _NullJoiner:
    '''A class to handle non-joinable values.'''

    def __init__(self, component_name, key):
        self.component_name = component_name
        self.key = key

    def join(self, vals):
        '''
        Either return the non-list value or raise an Exception.

        Arguments:
        vals - a list of values to process
        '''
        if len(vals) == 1:
            return vals[0]
        else:
            raise Exception(f"Cannot join multiple values for {self.component_name}.{self.key}")