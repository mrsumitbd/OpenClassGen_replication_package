class VasprunWrapper:
    '''VasprunWrapper class.

    This is used to fix broken vasprun.xml of VASP 5.2.8 at PRECFOCK.

    '''

    def __init__(self, fileptr):
        '''Init method.'''
        self.fileptr = fileptr
        self.buffer = ""
        self.eof = False

    def read(self, size=None):
        '''Replace broken PRECFOCK.'''
        if self.eof:
            return ""
        
        # Read data until we have enough or reach EOF
        while size is None or len(self.buffer) < size:
            chunk = self.fileptr.read(8192)
            if not chunk:
                self.eof = True
                break
            self.buffer += chunk
        
        if size is None:
            result = self.buffer
            self.buffer = ""
        else:
            result = self.buffer[:size]
            self.buffer = self.buffer[size:]
        
        # Fix broken PRECFOCK tags
        result = result.replace('<PRECFOCK>', '<PRECFOCK>\n')
        result = result.replace('</PRECFOCK>', '\n</PRECFOCK>')
        
        return result