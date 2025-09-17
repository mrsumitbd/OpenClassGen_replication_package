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
        v = self.validator
        if isinstance(v, set):
            return value in v
        if isinstance(v, type):
            try:
                v(value)
                return True
            except Exception:
                return False
        if callable(v):
            try:
                return bool(v(value))
            except Exception:
                return False
        return False