class BetaDist(object):
    '''
    Beta Distribusion for Thompson Sampling.
    '''

    def __init__(self, default_alpha=1, default_beta=1):
        '''
        Initialization

        Args:
            default_alpha:      Alpha
            default_beta:       Beta

        '''
        self.alpha = default_alpha
        self.beta = default_beta

    def observe(self, success, failure):
        '''
        Observation data.

        Args:
            success:      The number of success.
            failure:      The number of failure.

        '''
        self.alpha += success
        self.beta += failure

    def likelihood(self):
        '''
        Compute likelihood.

        Returns:
            likelihood.
        '''
        return random.betavariate(self.alpha, self.beta)

    def expected_value(self):
        '''
        Compute expected value.

        Returns:
            Expected value.
        '''
        return self.alpha / (self.alpha + self.beta)

    def variance(self):
        '''
        Compute variance.

        Returns:
            variance.
        '''
        return (self.alpha * self.beta) / ((self.alpha + self.beta) ** 2 * (self.alpha + self.beta + 1))