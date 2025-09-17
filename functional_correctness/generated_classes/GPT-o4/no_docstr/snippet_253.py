class EngineRef:
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r}, category={self.category!r})"

    def __eq__(self, other):
        if not isinstance(other, EngineRef):
            return NotImplemented
        return (self.name, self.category) == (other.name, other.category)

    def __hash__(self):
        return hash((self.name, self.category))