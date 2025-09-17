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

    Examples
    --------
    >>> from numdifftools.step_generators import BasicMaxStepGenerator
    >>> step_gen = BasicMaxStepGenerator(base_step=2.0, step_ratio=2,
    ...                                  num_steps=4)
    >>> [s for s in step_gen()]
    [2.0, 1.0, 0.5, 0.25]

    '''

    def __init__(self, base_step, step_ratio, num_steps, offset=0):
        self.base_step = base_step
        self.step_ratio = step_ratio
        self.num_steps = num_steps
        self.offset = offset

    def _range(self):
        return range(self.num_steps)

    def __call__(self):
        for i in self._range():
            yield self.base_step * (self.step_ratio ** (-i + self.offset))