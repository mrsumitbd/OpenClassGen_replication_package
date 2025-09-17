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

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def _tables_used(self):
        '''
        Tables injected into the step.

        Returns
        -------
        tables : set of str

        '''
        source = inspect.getsource(self.func)
        # Find patterns like tables['table_name'] or tables["table_name"]
        pattern = r'tables\[(["\'])([^"\']+)\1\]'
        matches = re.findall(pattern, source)
        # Extract just the table names (second group)
        tables = {match[1] for match in matches}
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
        filename = inspect.getsourcefile(self.func)
        lineno = inspect.getsourcelines(self.func)[1]
        source = inspect.getsource(self.func)
        return filename, lineno, source