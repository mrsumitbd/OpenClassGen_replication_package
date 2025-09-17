class abbreviated_step:
    '''
    Abbreviated XPath step. '.' or '..'
    '''

    def __init__(self, abbr):
        self.abbr = abbr

    def __repr__(self):
        return f"abbreviated_step('{self.abbr}')"

    def _serialize(self):
        return self.abbr

    def compute(self, ctx):
        if self.abbr == '.':
            return [ctx] if ctx is not None else []
        elif self.abbr == '..':
            if ctx is not None and hasattr(ctx, 'getparent'):
                parent = ctx.getparent()
                return [parent] if parent is not None else []
            return []
        return []

    def __call__(self, ctx):
        '''
        Alias for user convenience
        '''
        return self.compute(ctx)