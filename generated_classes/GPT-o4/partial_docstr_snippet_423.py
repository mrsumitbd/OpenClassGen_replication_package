class _StepFuncWrapper(object):
    '''
    Wrap a step function for argument matching.

    Parameters
    ----------
    step_name : str
    func : callable

    Attributes
    ----------
    name : str
        Name of step.

    '''

    def __init__(self, step_name, func):
        self.name = step_name
        self.func = func
        # Use the wrapped function's signature for argument matching
        self.__signature__ = inspect.signature(func)

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def _tables_used(self):
        '''
        Tables injected into the step.

        Returns
        -------
        tables : set of str

        '''
        return set(self.__signature__.parameters.keys())

    def func_source_data(self):
        '''
        Return data about a step function's source, including file name,
        line number, and source code.

        Returns
        -------
        filename : str
        lineno : int
            The line number on which the function starts.
        source : str

        '''
        filename = self.func.__code__.co_filename
        lineno = self.func.__code__.co_firstlineno
        try:
            source = inspect.getsource(self.func)
        except (OSError, IOError):
            source = None
        return filename, lineno, source