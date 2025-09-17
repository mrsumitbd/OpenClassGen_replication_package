class PRNG(object):
    """A Pseudorandom Number Generator that yields samples
    from the set of source blocks using the RSD degree
    distribution described above.
    """
    def __init__(self, params):
        self.K = int(params['K'])
        self.c = float(params['c'])
        self.delta = float(params['delta'])
        # LCG parameters
        self._mod = 2**31
        self._a = 1103515245
        self._inc = 12345
        self._state = params.get('seed', 1) % self._mod
        # compute RSD
        K, c, delta = self.K, self.c, self.delta
        R = c * math.log(K / delta) * math.sqrt(K)
        S = int(R)
        # ideal soliton rho
        rho = [0.0] * (K + 1)
        rho[1] = 1.0 / K
        for d in range(2, K + 1):
            rho[d] = 1.0 / (d * (d - 1))
        # spike tau
        tau = [0.0] * (K + 1)
        if S >= 1:
            bound = int(K / R)
            for d in range(1, bound):
                tau[d] = R / (d * K)
            if bound <= K:
                tau[bound] = R * math.log(R / delta) / K
        # combine and normalize
        beta = sum(rho[1:]) + sum(tau[1:])
        mu = [0.0] * (K + 1)
        for d in range(1, K + 1):
            mu[d] = (rho[d] + tau[d]) / beta
        # cumulative distribution
        cdf = [0.0] * (K + 1)
        cum = 0.0
        for d in range(1, K + 1):
            cum += mu[d]
            cdf[d] = cum
        cdf[K] = 1.0
        self._cdf = cdf

    def _get_next(self):
        self._state = (self._a * self._state + self._inc) % self._mod
        return self._state / float(self._mod)

    def _sample_d(self):
        u = self._get_next()
        # binary search in cdf
        lo, hi = 1, self.K
        while lo < hi:
            mid = (lo + hi) // 2
            if self._cdf[mid] < u:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def set_seed(self, seed):
        self._state = seed % self._mod

    def get_src_blocks(self, seed=None):
        if seed is not None:
            self.set_seed(seed)
        d = self._sample_d()
        K = self.K
        idx = list(range(K))
        for i in range(d):
            j = i + int(self._get_next() * (K - i))
            idx[i], idx[j] = idx[j], idx[i]
        return idx[:d]