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
        if self.kv_sep not in kv:
            return {}
        
        key_part, value = kv.split(self.kv_sep, 1)
        keys = key_part.split(self.keys_sep)
        
        result = {}
        current = result
        
        for key in keys[:-1]:
            current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        
        return result