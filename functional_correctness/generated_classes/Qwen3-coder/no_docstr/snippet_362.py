class SymbolForm(object):
    def __init__(self, name=None, grammar=None):
        self.name = name
        self.grammar = grammar
        self._attributes = {}

    def __getattr__(self, name):
        if name in self._attributes:
            return self._attributes[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __len__(self):
        return len(self._attributes)

    def __iter__(self):
        return iter(self._attributes)