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
        self._signature = inspect.signature(func)
        
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def _tables_used(self):
        '''
        Tables injected into the step.

        Returns
        -------
        tables : set of str

        '''
        tables = set()
        for param_name, param in self._signature.parameters.items():
            if param.annotation and hasattr(param.annotation, '__name__'):
                tables.add(param_name)
            elif param_name not in ['self', 'args', 'kwargs']:
                tables.add(param_name)
        return tables

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
        filename = inspect.getfile(self.func)
        lineno = inspect.getsourcelines(self.func)[1]
        source = inspect.getsource(self.func)
        return filename, lineno, source