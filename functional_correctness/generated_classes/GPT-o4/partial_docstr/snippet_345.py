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
        non_null = [v for v in vals if v is not None]
        if not non_null:
            return None
        if len(non_null) == 1:
            val = non_null[0]
            if isinstance(val, list):
                raise Exception(
                    f"Cannot join list for component '{self.component_name}' "
                    f"and key '{self.key}': got list {val}"
                )
            return val
        raise Exception(
            f"Multiple non-null values for component '{self.component_name}' "
            f"and key '{self.key}': {non_null}"
        )