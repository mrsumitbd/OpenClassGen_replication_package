class CauchyDistribution:
    '''Class to represent Cauchy distribution.'''

    def __init__(self, gamma):
        '''Init method.'''
        self.gamma = gamma

    def calc(self, x):
        '''Return Cauchy distribution.'''
        return 1 / (math.pi * self.gamma * (1 + (x / self.gamma) ** 2))