class PRNG(object):
    '''A Pseudorandom Number Generator that yields samples
    from the set of source blocks using the RSD degree
    distribution described above.
    '''

    def __init__(self, params):
        '''Provide RSD parameters on construction
        '''
        self.params = params
        self.K = params['K']  # number of source blocks
        self.S = params.get('S', 8)  # security parameter
        self.seed = None
        self._precompute_rsd()
        
    def _precompute_rsd(self):
        '''Precompute the RSD distribution'''
        K = self.K
        S = self.S
        
        # Ideal Soliton distribution
        rho = [0] * (K + 1)
        rho[1] = 1.0 / K
        for i in range(2, K + 1):
            rho[i] = 1.0 / (i * (i - 1))
        
        # Robust Soliton distribution
        R = S * math.ceil(math.sqrt(K * math.log(K) / S))
        tau = [0] * (K + 1)
        for i in range(1, min(R, K) + 1):
            tau[i] = S / (i * R)
        if R < K:
            tau[R] = math.log(K / R) * S / R
        
        # Combine distributions
        beta = sum(rho[i] + tau[i] for i in range(1, K + 1))
        self.rsd = [0] * (K + 1)
        for i in range(1, K + 1):
            self.rsd[i] = (rho[i] + tau[i]) / beta
    
    def _get_next(self):
        '''Executes the next iteration of the PRNG
        evolution process, and returns the result
        '''
        if self.seed is None:
            self.seed = random.randint(0, 2**32 - 1)
        
        # Simple linear congruential generator
        a = 1664525
        c = 1013904223
        m = 2**32
        self.seed = (a * self.seed + c) % m
        return self.seed / m

    def _sample_d(self):
        '''Samples degree given the precomputed
        distributions above and the linear PRNG output
        '''
        u = self._get_next()
        cumulative = 0.0
        for i in range(1, len(self.rsd)):
            cumulative += self.rsd[i]
            if u <= cumulative:
                return i
        return len(self.rsd) - 1

    def set_seed(self, seed):
        '''Reset the state of the PRNG to the 
        given seed
        '''
        self.seed = seed

    def get_src_blocks(self, seed=None):
        '''Returns the indices of a set of `d` source blocks
        sampled from indices i = 1, ..., K-1 uniformly, where
        `d` is sampled from the RSD described above.
        '''
        if seed is not None:
            self.set_seed(seed)
        
        d = self._sample_d()
        # Sample d distinct indices from 0 to K-1
        if d >= self.K:
            return list(range(self.K))
        else:
            return random.sample(range(self.K), d)