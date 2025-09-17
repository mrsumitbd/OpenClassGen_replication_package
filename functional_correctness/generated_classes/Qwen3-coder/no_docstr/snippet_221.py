class Result:
    def __init__(self):
        self._data = {}

    def __hash__(self):
        return hash(tuple(sorted(self._data.items())))

    def __eq__(self, other):
        if not isinstance(other, Result):
            return False
        return self._data == other._data

    def __copy__(self):
        import copy
        new_result = Result()
        new_result._data = copy.copy(self._data)
        return new_result

    def __repr__(self):
        return f"Result({self._data})"