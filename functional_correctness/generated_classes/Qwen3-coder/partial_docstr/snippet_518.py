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
        self.absolute = absolute
        
        # Set up random seed
        if seed is not None:
            self.random_state = random.Random(seed)
        else:
            self.random_state = random.Random()
            
        self.file_path = None

    def __enter__(self):
        # Generate random hex string
        hex_chars = '0123456789abcdef'
        random_hash = ''.join(self.random_state.choice(hex_chars) 
                             for _ in range(self.hash_length))
        
        # Create filename
        filename = self.prefix + random_hash + self.suffix
        
        # Get temporary directory
        if self.absolute:
            temp_dir = os.getcwd()
        else:
            temp_dir = ''
            
        self.file_path = os.path.join(temp_dir, filename)
        
        # Ensure the file exists by creating it
        with open(self.file_path, 'w'):
            pass
            
        return self.file_path

    def __exit__(self, *exc_info):
        # Remove the temporary file if it exists
        if self.file_path and os.path.exists(self.file_path):
            os.remove(self.file_path)
        return False