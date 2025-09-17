class CodeStatementGroup(object):
    '''This class is meant to provide common utility methods for
        objects that group multiple program statements together
        (e.g. functions, code blocks).

        It is not meant to be instantiated directly, only used for
        inheritance purposes.

        It defines the length of a statement group, and provides methods
        for integer-based indexing of program statements (as if using a list).
    '''

    def statement(self, i):
        '''Return the *i*-th statement from the object's `body`.'''
        return self.body[i]

    def statement_after(self, i):
        '''Return the statement after the *i*-th one, or `None`.'''
        if i + 1 < len(self.body):
            return self.body[i + 1]
        return None

    def __getitem__(self, i):
        '''Return the *i*-th statement from the object's `body`.'''
        return self.body[i]

    def __len__(self):
        '''Return the length of the statement group.'''
        return len(self.body)