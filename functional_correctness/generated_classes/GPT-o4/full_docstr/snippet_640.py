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
        self._g_function = g_function
        self._v_args = v_args
        self._d_args = d_args
        self._reset()

    def _reset(self):
        self._generator = self._g_function(*self._v_args, **self._d_args)

    def __iter__(self):
        '''x.__iter__() <==> iter(x)'''
        return self

    def next(self):
        '''x.next() -> the next value, or raise StopIteration'''
        try:
            return next(self._generator)
        except StopIteration:
            self._reset()
            return next(self._generator)

    __next__ = next