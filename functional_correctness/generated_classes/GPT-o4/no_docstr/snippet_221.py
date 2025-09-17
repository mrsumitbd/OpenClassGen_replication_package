class Result:
    def __init__(self):
        pass

    def __hash__(self):
        items = tuple(sorted(self.__dict__.items()))
        return hash(items)

    def __eq__(self, other):
        if not isinstance(other, Result):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __copy__(self):
        new = type(self)()
        for k, v in self.__dict__.items():
            setattr(new, k, v)
        return new

    def __repr__(self):
        items = ", ".join(f"{k}={v!r}" for k, v in sorted(self.__dict__.items()))
        return f"{self.__class__.__name__}({items})"