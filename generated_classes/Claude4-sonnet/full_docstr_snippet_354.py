class VasprunWrapper:
    '''VasprunWrapper class.

    This is used to fix broken vasprun.xml of VASP 5.2.8 at PRECFOCK.

    '''

    def __init__(self, fileptr):
        '''Init method.'''
        self.fileptr = fileptr

    def read(self, size=None):
        '''Replace broken PRECFOCK.'''
        if size is None:
            content = self.fileptr.read()
        else:
            content = self.fileptr.read(size)
        
        if isinstance(content, str):
            content = content.replace('PRECFOCK', 'PRECFOCK_FIXED')
        elif isinstance(content, bytes):
            content = content.replace(b'PRECFOCK', b'PRECFOCK_FIXED')
        
        return content