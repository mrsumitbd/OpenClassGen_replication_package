class Param(object):

    def __init__(self, name, fmt, types, required, validator, min_bed_fields=None):
        self.name = name
        self.fmt = fmt
        self.types = types
        self.required = required
        self.validator = validator
        self.min_bed_fields = min_bed_fields

    def __str__(self):
        return self.name

    def validate(self, value):
        if callable(self.validator):
            try:
                return self.validator(value)
            except:
                return False
        elif isinstance(self.validator, set):
            return value in self.validator
        elif isinstance(self.validator, type):
            try:
                self.validator(value)
                return True
            except:
                return False
        else:
            return True