class Define(object):
    '''
    Hold the defines and default-values.
    '''

    def __init__(self, definition):
        '''Initialize Define object.

        :param str definition: definition string. Ex: "INT -5 10"
        '''
        self.definition = definition
        self.original_definition = definition
        parts = definition.split()
        self.type = parts[0]
        self.default = None
        
        if self.type == "INT":
            self.min_val = int(parts[1])
            self.max_val = int(parts[2])
        elif self.type == "ENUM":
            self.values = parts[1:]
        elif self.type == "STRING":
            pass

    def safe_convert_str_to_int(self, inStr):
        '''Convert string to int safely. Check that it isn't float.

        :param str inStr: integer represented as string.
        :rtype: int
        '''
        if '.' in inStr:
            raise ValueError("Float value not allowed")
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
        if self.type == "ENUM":
            self.definition = self.type + " " + " ".join(self.values)