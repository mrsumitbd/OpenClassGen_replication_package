class _NameOnlyTemporaryFile(object):
    '''A context-managed temporary file which is not opened.

    The file should be accessible by name on any system.

    Parameters
    ----------
    suffix : string
        The suffix of the temporary file (default = '')
    prefix : string
        The prefix of the temporary file (default = '_tmp_')
    hash_length : string
        The length of the random hash.  The size of the hash space will
        be 16 ** hash_length (default=8)
    seed : integer
        the seed for the random number generator.  If not specified, the
        system time will be used as a seed.
    absolute : boolean
        If true, return an absolute path to a temporary file in the current
        working directory.

    Example
    -------

    >>> with _NameOnlyTemporaryFile(seed=0, absolute=False) as f:
    ...     print(f)
    ...
    _tmp_d82c07cd
    >>> os.path.exists('_tmp_d82c07cd')  # file removed after context
    False

    '''

    def __init__(self, prefix='_tmp_', suffix='', hash_length=8,
                 seed=None, absolute=True):
        self.prefix = prefix
        self.suffix = suffix
        self.hash_length = hash_length
        self.seed = seed
        self.absolute = absolute
        self.filename = None

    def __enter__(self):
        if self.seed is not None:
            random.seed(self.seed)
        
        hash_chars = '0123456789abcdef'
        hash_str = ''.join(random.choice(hash_chars) for _ in range(self.hash_length))
        
        self.filename = self.prefix + hash_str + self.suffix
        
        if self.absolute:
            self.filename = os.path.abspath(self.filename)
        
        with open(self.filename, 'w'):
            pass
        
        return self.filename

    def __exit__(self, *exc_info):
        if self.filename and os.path.exists(self.filename):
            os.remove(self.filename)