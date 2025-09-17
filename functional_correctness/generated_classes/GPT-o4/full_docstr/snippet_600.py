class ProgressBarStream:
    '''
    OutputStream wrapper to remove default linebreak at line endings.
    '''

    def __init__(self, stream):
        '''
        Wrap the given stream.
        '''
        self._stream = stream

    def write(self, *args, **kwargs):
        '''
        Call the stream's write method without linebreaks at line endings.
        '''
        if not args:
            return
        data = args[0]
        if isinstance(data, str):
            data = data.rstrip('\n')
            args = (data,) + args[1:]
        return self._stream.write(*args, **kwargs)

    def flush(self):
        '''
        Call the stream's flush method without any extra arguments.
        '''
        return self._stream.flush()