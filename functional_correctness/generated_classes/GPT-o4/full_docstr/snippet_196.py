class SeqPos(object):
    '''SeqPos - Sequence Position

    Each SeqAtom contains a SeqPos to locate the atom within the text
    sequence.
    '''

    def __init__(self, line=None, lineno=1, start=1, stop=None):
        '''Creates a new SeqPos from the given line in the sequence and start
        and stop character positions within the line.
        '''
        self.line = line
        self.lineno = lineno
        self.start = start
        self.stop = stop if stop is not None else start

    def __str__(self):
        '''Returns this SeqPos as a string.'''
        if self.start == self.stop:
            return f"{self.lineno}:{self.start}"
        return f"{self.lineno}:{self.start}-{self.stop}"