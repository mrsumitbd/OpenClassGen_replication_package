class ExampleClass(object):
    '''This ExampleClass does something magical.'''

    def __init__(self, test, *args, **kargs):
        '''
        # *args: list of arguments
        '''
        self.test = test
        self.args = args
        self.kargs = kargs

    def some_function(self):
        '''Example function inside a class.'''
        return "This is an example function"