class TextWrapper(object):
    '''Use this class if you have a binary-file but you want to
    write strings to it.
    '''

    def __init__(self, binary_file, encoding):
        '''Create a wrapper around :paramref:`binary_file` that encodes
        strings to bytes using :paramref:`encoding` and writes them
        to :paramref:`binary_file`.

        :param str encoding: The encoding to use to transfer the written string
          to bytes so they can be written to :paramref:`binary_file`
        :param binary_file: a file-like object open in binary mode
        '''
        self._binary_file = binary_file
        self._encoding = encoding

    def write(self, string):
        '''Write a string to the file.'''
        if not isinstance(string, str):
            raise TypeError("TextWrapper.write() argument must be a string")
        data = string.encode(self._encoding)
        return self._binary_file.write(data)