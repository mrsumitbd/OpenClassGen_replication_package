class VasprunWrapper:
    '''VasprunWrapper class.

    This is used to fix broken vasprun.xml of VASP 5.2.8 at PRECFOCK.

    '''

    def __init__(self, fileptr):
        '''Init method.'''
        raw = fileptr.read()
        # Remove the broken PRECFOCK section (misspelled closing tag </PRECFCOK>)
        self._data = re.sub(r"<PRECFOCK>.*?</PRECFCOK>", "", raw, flags=re.DOTALL)
        self._pos = 0

    def read(self, size=None):
        '''Replace broken PRECFOCK.'''
        if size is None:
            result = self._data[self._pos:]
            self._pos = len(self._data)
            return result
        else:
            end = self._pos + size
            result = self._data[self._pos:end]
            self._pos = min(end, len(self._data))
            return result