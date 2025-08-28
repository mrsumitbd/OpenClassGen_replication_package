class LogErrors:
    '''
    Wraps a function call to catch and report exceptions.
    '''

    def __init__(self, function, errors):
        '''
        :param function: the function to wrap
        :param errors: either a number, indicating how many errors to report
           before ignoring them, or one of these strings:
           'raise', meaning to raise an exception
           'ignore', meaning to ignore all errors
           'report', meaning to report all errors
        '''
        self.function = function
        self.errors = errors
        self.error_count = 0

    def __call__(self, *args, **kwds):
        '''
        Calls `self.function` with the given arguments and keywords, and
        returns its value - or if the call throws an exception, returns None.
        '''
        try:
            return self.function(*args, **kwds)
        except Exception as e:
            if self.errors == 'raise':
                raise
            elif self.errors == 'ignore':
                return None
            elif self.errors == 'report':
                print(f"Error in {self.function.__name__}: {e}")
                return None
            elif isinstance(self.errors, (int, float)):
                if self.error_count < self.errors:
                    print(f"Error in {self.function.__name__}: {e}")
                    self.error_count += 1
                return None
            else:
                return None