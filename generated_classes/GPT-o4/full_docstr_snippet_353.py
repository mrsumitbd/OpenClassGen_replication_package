class CauchyDistribution:
    '''Class to represent Cauchy distribution.'''

    def __init__(self, gamma):
        '''Init method.'''
        if not isinstance(gamma, (int, float)):
            raise TypeError("gamma must be a real number")
        if gamma <= 0:
            raise ValueError("gamma must be positive")
        self.gamma = float(gamma)

    def calc(self, x):
        '''Return Cauchy distribution.'''
        if not isinstance(x, (int, float)):
            raise TypeError("x must be a real number")
        gamma = self.gamma
        return (1.0 / (math.pi * gamma)) * (gamma*gamma / (x*x + gamma*gamma))