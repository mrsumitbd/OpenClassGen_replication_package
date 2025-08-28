class GenericColumn(object):
    def __init__(self, col_type, primary_key=False, unique=False, nullable=False):
        self.col_type = col_type
        self.primary_key = primary_key
        self.unique = unique
        self.nullable = nullable

    def check_type(self, value):
        if value is None:
            return self.nullable
        return isinstance(value, self.col_type)