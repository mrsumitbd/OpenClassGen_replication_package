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
            # Skip comments and empty lines
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Split by tab and strip whitespace from each field
            fields = [field.strip() for field in line.split('\t')]
            
            # Check if any field consists of only whitespace
            if any(field == '' for field in fields):
                raise ValueError("Field values consisting of only whitespace are not allowed")
            
            yield fields

    def close(self):
        '''
        Close the underlying stream.
        '''
        self.stream.close()