class SymbolForm(object):
    def __init__(self, name=None, grammar=None):
        self.name = name
        self.grammar = grammar
        self._symbols = []

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        symbol = SymbolForm(name, self.grammar)
        self._symbols.append(symbol)
        return symbol

    def __len__(self):
        return len(self._symbols)

    def __iter__(self):
        return iter(self._symbols)