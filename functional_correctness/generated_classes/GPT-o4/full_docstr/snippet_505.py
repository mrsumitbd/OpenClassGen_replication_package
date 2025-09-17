class FileReader(object):
    '''
    @summary: RSR File reader
    '''

    def __init__(self, f):
        '''
        @param f: {file} file pointer use to read
        '''
        if not hasattr(f, 'read'):
            raise ValueError("f must be a file-like object with a read method")
        self.f = f
        self._buffer = []

    def nextEvent(self):
        '''
        @summary: read next event and return it
        '''
        event = []
        # use any leftover lines first
        while self._buffer:
            line = self._buffer.pop(0)
            if line.strip() == '':
                if event:
                    return event
                else:
                    continue
            event.append(line.rstrip('\n'))

        for raw in self.f:
            if raw.strip() == '':
                if event:
                    return event
                else:
                    continue
            event.append(raw.rstrip('\n'))

        # end of file
        if event:
            return event
        return None