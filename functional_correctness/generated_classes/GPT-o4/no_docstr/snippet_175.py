class GenericColumn(object):
    def __init__(self, col_type, primary_key=False, unique=False, nullable=False):
        self.col_type = col_type
        self.primary_key = primary_key
        self.unique = unique
        self.nullable = nullable

    def check_type(self, value):
        if value is None:
            if self.nullable:
                return True
            raise ValueError("Null value not allowed for this column")
        if not isinstance(value, self.col_type):
            expected = (
                self.col_type.__name__
                if isinstance(self.col_type, type)
                else ", ".join(t.__name__ for t in self.col_type)
            )
            raise TypeError(f"Expected type {expected}, got {type(value).__name__}")
        return True