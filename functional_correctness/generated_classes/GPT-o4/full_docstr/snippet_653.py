class FitnessTransformation(object):
    '''This class does nothing but serve as an interface template.
    Typical use-case::

      f = FitnessTransformation(f, parameters_if_needed)

    See: class ``TransformSearchSpace``
    '''

    def __init__(self, fitness_function, *args, **kwargs):
        '''`fitness_function` must be callable (e.g. a function
        or a callable class instance)'''
        if not callable(fitness_function):
            raise TypeError("fitness_function must be callable")
        self._fitness = fitness_function
        self._args = args
        self._kwargs = kwargs

    def __call__(self, x, *args):
        '''identity as default transformation'''
        return self._fitness(x, *(self._args + args), **self._kwargs)