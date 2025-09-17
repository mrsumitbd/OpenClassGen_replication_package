class TsvReader(object):
    '''
    Represents a reader for tab-separated value files. Skips over comments 
    starting with #. Can be iterated over.

    Field values consisting of only whitespace are not allowed.
    '''

    def __init__(self, stream):
        '''
            Make a new TsvReader to read from the given stream.
        '''
        self.stream = stream

    def __iter__(self):
        '''
            Yields lists of all fields on each line, as strings, until all lines are
            exhausted. Strips whitespace around field contents. 
        '''
        for line in self.stream:
            if line.startswith('#'):
                continue
            line = line.rstrip('\n')
            fields = line.split('\t')
            stripped_fields = []
            for f in fields:
                s = f.strip()
                if s == '':
                    raise ValueError("Field value consists only of whitespace or is empty")
                stripped_fields.append(s)
            yield stripped_fields

    def close(self):
        '''
            Close the underlying stream.
        '''
        self.stream.close()