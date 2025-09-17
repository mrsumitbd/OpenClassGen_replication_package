class abbreviated_step:
    '''
    Abbreviated XPath step. '.' or '..'
    '''

    def __init__(self, abbr):
        if abbr not in ('.', '..'):
            raise ValueError(f"Invalid abbreviated step {abbr!r}, expected '.' or '..'")
        self.abbr = abbr

    def __repr__(self):
        return f"{self.__class__.__name__}({self.abbr!r})"

    def _serialize(self):
        return self.abbr

    def compute(self, ctx):
        node = getattr(ctx, 'node', None)
        if node is None:
            return []
        if self.abbr == '.':
            return [node]
        # '..'
        parent = None
        # try lxml-style
        if hasattr(node, 'getparent'):
            parent = node.getparent()
        # fallback to ElementTree if it stores parent in ._parent
        elif hasattr(node, '_parent'):
            parent = node._parent
        return [parent] if parent is not None else []

    def __call__(self, ctx):
        '''
        Alias for user convenience
        '''
        return self.compute(ctx)