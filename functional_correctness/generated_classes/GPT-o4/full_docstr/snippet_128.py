class ExampleClass(object):
    '''This ExampleClass does something magical.'''

    def __init__(self, test, *args, **kargs):
        '''
        # *args: list of functions to apply in sequence
        # **kargs: dict of named functions to apply after args
        '''
        self.test = test
        self.args = list(args)
        self.kargs = kargs

    def some_function(self):
        '''Example function inside a class.'''
        result = self.test
        for fn in self.args:
            if callable(fn):
                result = fn(result)
        for fn in self.kargs.values():
            if callable(fn):
                result = fn(result)
        return result

    def __repr__(self):
        return "ExampleClass(test={!r}, args={!r}, kargs={!r})".format(
            self.test, self.args, self.kargs
        )