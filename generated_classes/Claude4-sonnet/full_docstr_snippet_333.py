class PRNG(object):
    '''A Pseudorandom Number Generator that yields samples
    from the set of source blocks using the RSD degree
    distribution described above.
    '''

    def __init__(self, params):
        '''Provide RSD parameters on construction
        '''
        self.K = params['K']
        self.c = params.get('c', 0.1)
        self.delta = params.get('delta', 0.5)
        self.state = 1
        self._precompute_distributions()

    def _precompute_distributions(self):
        '''Precompute the RSD distribution'''
        import math
        
        # Ideal soliton distribution
        rho = [0] * (self.K + 1)
        rho[1] = 1.0 / self.K
        for i in range(2, self.K + 1):
            rho[i] = 1.0 / (i * (i - 1))
        
        # Robust soliton distribution
        R = self.c * math.log(self.K / self.delta) * math.sqrt(self.K)
        tau = [0] * (self.K + 1)
        
        for i in range(1, int(self.K / R) + 1):
            tau[i] = R / (i * self.K)
        tau[int(self.K / R)] = R * math.log(R / self.delta) / self.K
        
        # Combine distributions
        mu = [rho[i] + tau[i] for i in range(self.K + 1)]
        beta = sum(mu)
        
        # Normalize
        self.distribution = [mu[i] / beta for i in range(self.K + 1)]
        
        # Create cumulative distribution
        self.cumulative = [0] * (self.K + 1)
        for i in range(1, self.K + 1):
            self.cumulative[i] = self.cumulative[i-1] + self.distribution[i]

    def _get_next(self):
        '''Executes the next iteration of the PRNG
        evolution process, and returns the result
        '''
        # Linear congruential generator
        a = 1664525
        c = 1013904223
        m = 2**32
        self.state = (a * self.state + c) % m
        return self.state / m

    def _sample_d(self):
        '''Samples degree given the precomputed
        distributions above and the linear PRNG output
        '''
        rand_val = self._get_next()
        for i in range(1, self.K + 1):
            if rand_val <= self.cumulative[i]:
                return i
        return self.K

    def set_seed(self, seed):
        '''Reset the state of the PRNG to the 
        given seed
        '''
        self.state = seed if seed is not None else 1

    def get_src_blocks(self, seed=None):
        '''Returns the indices of a set of `d` source blocks
        sampled from indices i = 1, ..., K-1 uniformly, where
        `d` is sampled from the RSD described above.
        '''
        if seed is not None:
            self.set_seed(seed)
        
        d = self._sample_d()
        blocks = set()
        
        while len(blocks) < d:
            rand_val = self._get_next()
            block_idx = int(rand_val * self.K)
            if block_idx == 0:
                block_idx = 1
            blocks.add(block_idx)
        
        return list(blocks)