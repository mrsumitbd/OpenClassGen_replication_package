class ConstRandnShift(object):
    '''``ConstRandnShift()(x)`` adds a fixed realization of
    ``stddev * randn(len(x))`` to the vector x.

    By default, the realized shift is the same for each instance of
    ``ConstRandnShift``, see ``seed`` argument. This class is used in
    class ``FFWrapper.ShiftedFitness`` as default transformation.

    See: class ``FFWrapper.ShiftedFitness``

    '''

    def __init__(self, stddev=3, seed=1):
        '''with ``seed=None`` each instance realizes a different shift'''
        self.stddev = stddev
        self.seed = seed
        self.shift = None

    def __call__(self, x):
        '''return "shifted" ``x - shift``

        '''
        x = np.array(x)
        if self.shift is None or len(self.shift) != len(x):
            if self.seed is not None:
                np.random.seed(self.seed)
            self.shift = self.stddev * np.random.randn(len(x))
        return x - self.shift

    def get(self, dimension):
        '''return shift applied to ``zeros(dimension)``

            >>> import numpy as np, cma
            >>> s = cma.ConstRandnShift()
            >>> assert all(s(-s.get(3)) == np.zeros(3))
            >>> assert all(s.get(3) == s(np.zeros(3)))

        '''
        if self.shift is None or len(self.shift) != dimension:
            if self.seed is not None:
                np.random.seed(self.seed)
            self.shift = self.stddev * np.random.randn(dimension)
        return self.shift