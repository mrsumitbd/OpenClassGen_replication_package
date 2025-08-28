class Define(object):
    '''
    Hold the defines and default-values.
    '''

    def __init__(self, definition):
        '''Initialize Define object.

        :param str definition: definition string. Ex: "INT -5 10"
        '''
        self.definition = definition.strip()
        parts = self.definition.split()
        if not parts:
            raise ValueError("Empty definition")
        self._type = parts[0].upper()
        self._default = None

        if self._type == "INT":
            if len(parts) != 3:
                raise ValueError("INT definition must have exactly two bounds")
            self._min = self.safe_convert_str_to_int(parts[1])
            self._max = self.safe_convert_str_to_int(parts[2])
        elif self._type == "ENUM":
            if len(parts) < 2:
                raise ValueError("ENUM definition must have at least one value")
            # store enum values in order
            self.enums = parts[1:]
        else:
            # for other types just keep raw parts
            self._params = parts[1:]

    @staticmethod
    def safe_convert_str_to_int(inStr):
        '''Convert string to int safely. Check that it isn't float.

        :param str inStr: integer represented as string.
        :rtype: int
        '''
        s = inStr.strip()
        if not s:
            raise ValueError("Empty string cannot be converted to int")
        # Reject floats like "1.0" or "2e3"
        if any(c in s for c in ('.', 'e', 'E')):
            raise ValueError(f"String '{inStr}' looks like a float, not an int")
        try:
            return int(s)
        except ValueError:
            raise ValueError(f"Cannot convert '{inStr}' to int")

    def set_default(self, default):
        '''Set Definition default value.

        :param default: default value; number, str or quoted str ("value")
        '''
        # If it's a quoted string, strip quotes
        if isinstance(default, str) and len(default) >= 2 and default[0] == '"' and default[-1] == '"':
            val = default[1:-1]
        else:
            val = default

        if self._type == "INT":
            # try converting to int
            try:
                ival = self.safe_convert_str_to_int(str(val))
            except ValueError:
                raise ValueError("Default for INT must be integer")
            if ival < self._min or ival > self._max:
                raise ValueError(f"Default {ival} out of bounds [{self._min}, {self._max}]")
            self._default = ival

        elif self._type == "ENUM":
            # default must be one of enums
            if val not in self.enums:
                raise ValueError(f"Default '{val}' not in ENUM values {self.enums}")
            self._default = val

        else:
            # for other types, accept as-is
            self._default = val

    def update(self):
        '''Update definition string for type ENUM.

        For type ENUM rebuild the definition string from current values. Otherwise do nothing.
        '''
        if self._type == "ENUM":
            self.definition = "ENUM " + " ".join(self.enums)