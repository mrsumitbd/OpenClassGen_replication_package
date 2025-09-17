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
        result = f"{self.linter_name}: {self.path}"
        if self.line_nr is not None:
            result += f":{self.line_nr}"
            if self.col is not None:
                result += f":{self.col}"
        result += f": {self.msg}"
        return result

    def _cmp_key(self, obj=None):
        '''Comparison key for sorting results from all linters.

        The sort should group files and lines from different linters to make it
        easier for refactoring.
        '''
        return (self.path, self.line_nr or 0, self.col or 0, self.linter_name)

    def __lt__(self, other):
        '''Use ``_cmp_key`` to compare two lines.'''
        return self._cmp_key() < other._cmp_key()