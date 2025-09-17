class BetaDist(object):
    '''
    Beta Distribution for Thompson Sampling.
    '''

    def __init__(self, default_alpha=1, default_beta=1):
        '''
        Initialization

        Args:
            default_alpha: Alpha
            default_beta:  Beta
        '''
        self.default_alpha = default_alpha
        self.default_beta = default_beta
        self.alpha = default_alpha
        self.beta = default_beta

    def observe(self, success, failure):
        '''
        Observation data.

        Args:
            success: The number of successes.
            failure: The number of failures.
        '''
        self.alpha += success
        self.beta += failure

    def likelihood(self):
        '''
        Compute likelihood (normalization constant B(alpha, beta)).

        Returns:
            likelihood.
        '''
        return math.gamma(self.alpha) * math.gamma(self.beta) / math.gamma(self.alpha + self.beta)

    def expected_value(self):
        '''
        Compute expected value.

        Returns:
            Expected value.
        '''
        total = self.alpha + self.beta
        return self.alpha / total if total > 0 else 0

    def variance(self):
        '''
        Compute variance.

        Returns:
            variance.
        '''
        total = self.alpha + self.beta
        return (self.alpha * self.beta) / (total**2 * (total + 1)) if total > 0 else 0