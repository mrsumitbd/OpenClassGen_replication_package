class Pdf(object):
    '''Represents a probability density function (PDF).'''

    def Density(self, x):
        '''Evaluates this Pdf at x.

        Returns: float probability density
        '''
        raise NotImplementedError('Density must be implemented by subclasses')

    def MakePmf(self, xs, name=''):
        '''Makes a discrete version of this Pdf, evaluated at xs.

        xs: equally-spaced sequence of values

        Returns: new Pmf
        '''
        pmf = Pmf(name=name)
        if not xs:
            return pmf
        dx = xs[1] - xs[0] if len(xs) > 1 else 1.0
        for x in xs:
            pmf[x] = self.Density(x) * dx
        pmf.Normalize()
        return pmf