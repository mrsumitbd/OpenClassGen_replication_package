class EngineRef:
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category

    def __repr__(self):
        return f"EngineRef(name='{self.name}', category='{self.category}')"

    def __eq__(self, other):
        if not isinstance(other, EngineRef):
            return False
        return self.name == other.name and self.category == other.category

    def __hash__(self):
        return hash((self.name, self.category))