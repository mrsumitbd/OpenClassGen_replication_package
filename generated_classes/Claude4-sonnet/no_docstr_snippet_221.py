class Result:
    def __init__(self, value=None, error=None):
        self.value = value
        self.error = error
        self.is_success = error is None

    def __hash__(self):
        return hash((self.value, self.error, self.is_success))

    def __eq__(self, other):
        if not isinstance(other, Result):
            return False
        return (self.value == other.value and 
                self.error == other.error and 
                self.is_success == other.is_success)

    def __copy__(self):
        return Result(self.value, self.error)

    def __repr__(self):
        if self.is_success:
            return f"Result(value={repr(self.value)})"
        else:
            return f"Result(error={repr(self.error)})"