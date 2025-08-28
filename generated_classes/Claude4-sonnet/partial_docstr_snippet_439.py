class Pdf(object):
    '''Represents a probability density function (PDF).'''

    def Density(self, x):
        '''Evaluates this Pdf at x.

        Returns: float probability density
        '''
        pass

    def MakePmf(self, xs, name=''):
        '''Makes a discrete version of this Pdf, evaluated at xs.

        xs: equally-spaced sequence of values

        Returns: new Pmf
        '''
        pmf = Pmf(name=name)
        for x in xs:
            pmf.Set(x, self.Density(x))
        pmf.Normalize()
        return pmf