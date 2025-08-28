class Define(object):
    '''
    Hold the defines and default-values.
    '''

    def __init__(self, definition):
        '''Initialize Define object.

        :param str definition: definition string. Ex: "INT -5 10"
        '''
        self.definition = definition
        self.default = None
        parts = definition.split()
        if parts:
            self.type = parts[0]
            if self.type == 'ENUM':
                self.values = parts[1:]
            elif len(parts) >= 3:
                self.min_val = self.safe_convert_str_to_int(parts[1])
                self.max_val = self.safe_convert_str_to_int(parts[2])
    
    def safe_convert_str_to_int(self, inStr):
        '''Convert string to int safely. Check that it isn't float.

        :param str inStr: integer represented as string.
        :rtype: int
        '''
        if '.' in inStr:
            raise ValueError("String represents a float, not an integer")
        return int(inStr)

    def set_default(self, default):
        '''Set Definition default value.

        :param default: default value; number, str or quoted str ("value")
        '''
        self.default = default

    def update(self):
        '''Update definition string for type ENUM.

        For type ENUM rebuild the definition string from current values. Otherwise do nothing.
        '''
        if self.type == 'ENUM':
            self.definition = 'ENUM ' + ' '.join(self.values)