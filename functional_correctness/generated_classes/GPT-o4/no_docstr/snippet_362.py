class SymbolForm(object):
    def __init__(self, name=None, grammar=None):
        self.name = name
        # Normalize grammar into a dict: {child_name: child_grammar_or_None}
        if grammar is None:
            self.grammar = {}
        elif isinstance(grammar, dict):
            self.grammar = grammar.copy()
        else:
            try:
                self.grammar = {k: None for k in grammar}
            except TypeError:
                raise TypeError("grammar must be None, a dict, or an iterable of names")
        self._children = {}

    def __getattr__(self, name):
        if name in self.grammar:
            if name not in self._children:
                child_grammar = self.grammar[name]
                self._children[name] = SymbolForm(name=name, grammar=child_grammar)
            return self._children[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __len__(self):
        return len(self.grammar)

    def __iter__(self):
        for child_name in self.grammar:
            yield getattr(self, child_name)