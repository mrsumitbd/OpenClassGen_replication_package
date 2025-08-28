class FileReader(object):
    '''
    @summary: RSR File reader
    '''

    def __init__(self, f):
        '''
        @param f: {file} file pointer use to read
        '''
        self.file = f
        self.finished = False

    def nextEvent(self):
        '''
        @summary: read next event and return it
        '''
        if self.finished:
            return None
            
        try:
            line = self.file.readline()
            if not line:
                self.finished = True
                return None
            return line.strip()
        except Exception:
            self.finished = True
            return None