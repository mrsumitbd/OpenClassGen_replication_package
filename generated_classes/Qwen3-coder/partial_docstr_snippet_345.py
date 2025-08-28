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
        elif len(vals) == 0:
            raise Exception(f"No values to join for {self.component_name}.{self.key}")
        else:
            raise Exception(f"Multiple values found for non-joinable field {self.component_name}.{self.key}: {vals}")