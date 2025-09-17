class Pdf(object):
    '''Represents a probability density function (PDF).'''

    def Density(self, x):
        '''Evaluates this Pdf at x.

        Returns: float probability density
        '''
        raise NotImplementedError

    def MakePmf(self, xs, name=''):
        '''Makes a discrete version of this Pdf, evaluated at xs.

        xs: equally-spaced sequence of values

        Returns: new Pmf
        '''
        from collections import Counter
        
        # Evaluate the PDF at each point in xs
        probs = [self.Density(x) for x in xs]
        
        # Create a PMF with these values
        pmf = Pmf(dict(zip(xs, probs)), name=name)
        return pmf