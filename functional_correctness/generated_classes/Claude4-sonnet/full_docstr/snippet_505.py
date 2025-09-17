class FileReader(object):
    '''
    @summary: RSR File reader
    '''

    def __init__(self, f):
        '''
        @param f: {file} file pointer use to read
        '''
        self.file = f
        self.current_position = 0

    def nextEvent(self):
        '''
        @summary: read next event and return it
        '''
        if self.file.closed:
            return None
        
        line = self.file.readline()
        if not line:
            return None
        
        self.current_position = self.file.tell()
        return line.strip()