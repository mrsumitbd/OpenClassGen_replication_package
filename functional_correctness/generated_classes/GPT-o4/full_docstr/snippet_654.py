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
        if seed is None:
            self.rng = np.random.RandomState()
        else:
            self.rng = np.random.RandomState(seed)
        self._shifts = {}

    def __call__(self, x):
        '''return "shifted" ``x + shift``'''
        x = np.asanyarray(x)
        d = x.shape[0]
        if d not in self._shifts:
            self._shifts[d] = self.stddev * self.rng.randn(d)
        return x + self._shifts[d]

    def get(self, dimension):
        '''return shift applied to ``zeros(dimension)``

                >>> import numpy as np, cma
                >>> s = cma.ConstRandnShift()
                >>> assert all(s(-s.get(3)) == np.zeros(3))
                >>> assert all(s.get(3) == s(np.zeros(3)))

        '''
        if dimension not in self._shifts:
            self._shifts[dimension] = self.stddev * self.rng.randn(dimension)
        return self._shifts[dimension]