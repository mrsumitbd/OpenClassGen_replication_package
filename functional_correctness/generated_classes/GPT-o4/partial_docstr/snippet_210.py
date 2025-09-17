class ConsistentHash(object):
    ''' ConsistentHash(n,r) creates a consistent hash object for a
        cluster of size n, using r replicas.

        It has three attributes. num_machines and num_replics are
        self-explanatory.  hash_tuples is a list of tuples (j,k,hash),
        where j ranges over machine numbers (0...n-1), k ranges over
        replicas (0...r-1), and hash is the corresponding hash value,
        in the range [0,1).  The tuples are sorted by increasing hash
        value.

        The class has a single instance method, get_machine(key), which
        returns the number of the machine to which key should be
        mapped.
    '''

    def __init__(self, num_machines=1, num_replicas=1):
        self.num_machines = num_machines
        self.num_replicas = num_replicas
        # build and sort all (machine, replica, hash) tuples
        self.hash_tuples = []
        for j in range(self.num_machines):
            for k in range(self.num_replicas):
                h = self.hash(f"{j}-{k}")
                self.hash_tuples.append((j, k, h))
        self.hash_tuples.sort(key=lambda t: t[2])
        # extract sorted hash list for bisection
        self._sorted_hashes = [t[2] for t in self.hash_tuples]

    def get_machine(self, key):
        ''' Returns the number of the machine which key gets sent to.
        '''
        h_key = self.hash(key)
        idx = bisect.bisect_left(self._sorted_hashes, h_key)
        if idx == len(self._sorted_hashes):
            idx = 0
        machine, _, _ = self.hash_tuples[idx]
        return machine

    @classmethod
    def hash(cls, key):
        ''' hash(key) returns a hash in the range [0,1)
        '''
        # normalize key to bytes
        if isinstance(key, bytes):
            key_bytes = key
        elif isinstance(key, str):
            key_bytes = key.encode('utf-8')
        else:
            key_bytes = str(key).encode('utf-8')
        # compute MD5 digest and map to [0,1)
        digest = hashlib.md5(key_bytes).digest()
        intval = int.from_bytes(digest, byteorder='big')
        return intval / float(1 << (8 * len(digest)))