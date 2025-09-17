class ConsistentHash(object):
    ''' ConsistentHash(n,r) creates a consistent hash object for a
        cluster of size n, using r replicas.

        It has three attributes. num_machines and num_replicas are
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
        self.hash_tuples = []
        
        for j in range(num_machines):
            for k in range(num_replicas):
                hash_value = self.hash(f"{j},{k}")
                self.hash_tuples.append((j, k, hash_value))
        
        self.hash_tuples.sort(key=lambda x: x[2])

    def get_machine(self, key):
        ''' Returns the number of the machine which key gets sent to.
        '''
        if not self.hash_tuples:
            return None
            
        key_hash = self.hash(key)
        
        # Binary search for the first hash >= key_hash
        left, right = 0, len(self.hash_tuples)
        while left < right:
            mid = (left + right) // 2
            if self.hash_tuples[mid][2] < key_hash:
                left = mid + 1
            else:
                right = mid
        
        # If we've gone past the end, wrap around to the beginning
        if left == len(self.hash_tuples):
            left = 0
            
        return self.hash_tuples[left][0]

    @classmethod
    def hash(cls, key):
        ''' hash(key) returns a hash in the range [0,1)
        '''
        from hashlib import md5
        return int(md5(key.encode()).hexdigest(), 16) / (2**128)