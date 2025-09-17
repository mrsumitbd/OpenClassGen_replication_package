class LinterOutput:
    '''A one-line linter result. It can be sorted and printed as string.'''

    def __init__(self, linter_name, path, msg, line_nr=None, col=None):
        '''Optionally set all attributes.

        Args:
            path (str): Relative file path.
            line (int): Line number.
            msg (str): Explanation of what is wrong.
            col (int): Column where the problem begins.

        '''
        self.linter_name = linter_name
        self.path = path
        self.msg = msg
        self.line_nr = line_nr
        self.col = col

    def __str__(self):
        '''Output shown to the user.'''
        parts = [self.path]
        if self.line_nr is not None:
            parts.append(str(self.line_nr))
            if self.col is not None:
                parts.append(str(self.col))
        parts.append(self.msg)
        return ':'.join(parts)

    def _cmp_key(self, obj=None):
        '''Comparison key for sorting results from all linters.

        The sort should group files and lines from different linters to make it
        easier for refactoring.
        '''
        if obj is None:
            return (self.path or '', self.line_nr or 0, self.col or 0, self.linter_name or '')
        else:
            return (
                (self.path or '', self.line_nr or 0, self.col or 0, self.linter_name or ''),
                (obj.path or '', obj.line_nr or 0, obj.col or 0, obj.linter_name or '')
            )

    def __lt__(self, other):
        '''Use ``_cmp_key`` to compare two lines.'''
        self_key, other_key = self._cmp_key(other)
        return self_key < other_key