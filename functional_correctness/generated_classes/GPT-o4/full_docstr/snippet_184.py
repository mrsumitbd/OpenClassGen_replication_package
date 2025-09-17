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
        if isinstance(errors, str):
            if errors not in ('raise', 'ignore', 'report'):
                raise ValueError("errors must be 'raise', 'ignore', 'report', or a non-negative integer")
            self.mode = errors
        else:
            try:
                count = int(errors)
            except Exception:
                raise TypeError("errors must be a string or an integer")
            if count < 0:
                raise ValueError("error count must be non-negative")
            self.mode = 'count'
            self.errors_allowed = count
            self.error_count = 0

    def __call__(self, *args, **kwds):
        '''
        Calls `self.function` with the given arguments and keywords, and
        returns its value - or if the call throws an exception, returns None.
        '''
        try:
            return self.function(*args, **kwds)
        except Exception:
            if self.mode == 'raise':
                raise
            if self.mode == 'ignore':
                return None
            if self.mode == 'report':
                traceback.print_exc()
                return None
            # mode == 'count'
            if self.error_count < self.errors_allowed:
                traceback.print_exc()
                self.error_count += 1
            return None