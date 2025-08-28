class BasicMaxStepGenerator(object):
    '''
    Generates a sequence of steps of decreasing magnitude

    where
        steps = base_step * step_ratio ** (-i + offset)

    for i=0, 1,.., num_steps-1.


    Parameters
    ----------
    base_step : float, array-like.
       Defines the start step, i.e., maximum step
    step_ratio : real scalar.
        Ratio between sequential steps generated.  Note: Ratio > 1
    num_steps : scalar integer.
        defines number of steps generated.
    offset : real scalar, optional, default 0
        offset to the base step
    '''
    def __init__(self, base_step, step_ratio, num_steps, offset=0):
        self.base_step = np.asarray(base_step, dtype=float)
        if not np.isscalar(step_ratio) or step_ratio <= 1:
            raise ValueError("step_ratio must be a scalar greater than 1")
        if not isinstance(num_steps, int) or num_steps < 0:
            raise ValueError("num_steps must be a non-negative integer")
        self.step_ratio = float(step_ratio)
        self.num_steps = num_steps
        self.offset = float(offset)

    def _range(self):
        return (self.step_ratio ** (-i + self.offset) for i in range(self.num_steps))

    def __call__(self):
        for r in self._range():
            yield self.base_step * r