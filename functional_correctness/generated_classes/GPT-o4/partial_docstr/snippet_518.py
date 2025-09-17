class _NameOnlyTemporaryFile(object):
    '''A context-managed temporary file which is not opened.

    The file should be accessible by name on any system.

    Parameters
    ----------
    suffix : string
        The suffix of the temporary file (default = '')
    prefix : string
        The prefix of the temporary file (default = '_tmp_')
    hash_length : integer
        The length of the random hash.  The size of the hash space will
        be 16 ** hash_length (default=8)
    seed : integer
        the seed for the random number generator.  If not specified, the
        system time will be used as a seed.
    absolute : boolean
        If true, return an absolute path to a temporary file in the current
        working directory.
    '''
    def __init__(self, prefix='_tmp_', suffix='', hash_length=8,
                 seed=None, absolute=True):
        self.prefix = prefix
        self.suffix = suffix
        self.hash_length = hash_length
        # initialize RNG
        if seed is None:
            self._rng = random.Random()
        else:
            self._rng = random.Random(seed)
        self.absolute = absolute
        self.name = None

    def __enter__(self):
        # generate a unique filename
        while True:
            # random hex string of given length
            rand_int = self._rng.getrandbits(4 * self.hash_length)
            hash_str = format(rand_int, '0{}x'.format(self.hash_length))
            base = f"{self.prefix}{hash_str}{self.suffix}"
            if self.absolute:
                candidate = os.path.abspath(base)
            else:
                candidate = base
            if not os.path.exists(candidate):
                break
        # create the file by touching it
        open(candidate, 'a').close()
        self.name = candidate
        return self.name

    def __exit__(self, *exc_info):
        try:
            if self.name and os.path.exists(self.name):
                os.remove(self.name)
        except Exception:
            pass
        # propagate exceptions if any
        return False