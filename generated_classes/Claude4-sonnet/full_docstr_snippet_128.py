class ExampleClass(object):
    '''This ExampleClass does something magical.'''

    def __init__(self, test, *args, **kwargs):
        '''
        # *args: list of arguments
        '''
        self.test = test
        self.args = args
        self.kwargs = kwargs

    def some_function(self):
        '''Example function inside a class.'''
        return f"Test: {self.test}, Args: {self.args}, Kwargs: {self.kwargs}"