class FitnessTransformation(object):
    '''This class does nothing but serve as an interface template.
    Typical use-case::

      f = FitnessTransformation(f, parameters_if_needed)``

    See: class ``TransformSearchSpace``

    '''

    def __init__(self, fitness_function, *args, **kwargs):
        '''`fitness_function` must be callable (e.g. a function
        or a callable class instance)'''
        self.fitness_function = fitness_function
        self.args = args
        self.kwargs = kwargs

    def __call__(self, x, *args):
        '''identity as default transformation'''
        return self.fitness_function(x, *args)