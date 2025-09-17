class KVParser(object):
    def __init__(self, kv_sep='=', keys_sep='.'):
        self.kv_sep = kv_sep
        self.keys_sep = keys_sep

    def parse(self, kv):
        '''
        Parses key value string into dict

        Examples:
            >> parser.parse('test1.test2=value')
            {'test1': {'test2': 'value'}}

            >> parser.parse('test=value')
            {'test': 'value'}
        '''
        key_str, value = kv.split(self.kv_sep, 1)
        parts = key_str.split(self.keys_sep) if self.keys_sep else [key_str]
        result = current = {}
        for part in parts[:-1]:
            current[part] = {}
            current = current[part]
        current[parts[-1]] = value
        return result