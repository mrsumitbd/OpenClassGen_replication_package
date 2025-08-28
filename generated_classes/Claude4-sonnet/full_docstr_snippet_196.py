class SeqPos(object):
    '''SeqPos - Sequence Position

    Each SeqAtom contains a SeqPos to locate the atom within the text
    sequence.
    '''

    def __init__(self, line=None, lineno=1, start=1, stop=None):
        '''Creates a new SeqPos from the given line in the sequence and start
        and stop line and character positions within the line.
        '''
        self.line = line
        self.lineno = lineno
        self.start = start
        self.stop = stop

    def __str__(self):
        '''Returns this SeqPos as a string.'''
        return f"SeqPos(line={self.line!r}, lineno={self.lineno}, start={self.start}, stop={self.stop})"