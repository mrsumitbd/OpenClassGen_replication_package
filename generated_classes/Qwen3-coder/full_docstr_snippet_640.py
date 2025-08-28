class Regenerator(object):
    '''
    Calls a generator and iterates it. When it's finished iterating, the
    generator is called again. This allows you to iterate a generator more
    than once (well, sort of).
    '''

    def __init__(self, g_function, *v_args, **d_args):
        '''
        @type  g_function: function
        @param g_function: Function that when called returns a generator.

        @type  v_args: tuple
        @param v_args: Variable arguments to pass to the generator function.

        @type  d_args: dict
        @param d_args: Variable arguments to pass to the generator function.
        '''
        self.g_function = g_function
        self.v_args = v_args
        self.d_args = d_args
        self.generator = None

    def __iter__(self):
        '''x.__iter__() <==> iter(x)'''
        return self

    def next(self):
        '''x.next() -> the next value, or raise StopIteration'''
        if self.generator is None:
            self.generator = self.g_function(*self.v_args, **self.d_args)
        
        try:
            return next(self.generator)
        except StopIteration:
            self.generator = None
            raise

    def __next__(self):
        '''Python 3 compatibility'''
        return self.next()