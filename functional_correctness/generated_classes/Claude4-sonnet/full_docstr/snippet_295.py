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
            line = line.rstrip('\n\r')
            if line.startswith('#') or not line.strip():
                continue
            fields = []
            for field in line.split('\t'):
                stripped_field = field.strip()
                if not stripped_field:
                    raise ValueError("Field values consisting of only whitespace are not allowed")
                fields.append(stripped_field)
            yield fields

    def close(self):
        '''
        Close the underlying stream.
        '''
        self.stream.close()