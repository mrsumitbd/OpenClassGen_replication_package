class abbreviated_step:
    '''
    Abbreviated XPath step. '.' or '..'
    '''

    def __init__(self, abbr):
        if abbr not in ('.', '..'):
            raise ValueError("Abbreviated step must be '.' or '..'")
        self.abbr = abbr

    def __repr__(self):
        return f"abbreviated_step('{self.abbr}')"

    def _serialize(self):
        return self.abbr

    def compute(self, ctx):
        if self.abbr == '.':
            return [ctx.node]
        else:  # self.abbr == '..'
            parent = ctx.node.getparent()
            return [parent] if parent is not None else []

    def __call__(self, ctx):
        '''
        Alias for user convenience
        '''
        return self.compute(ctx)