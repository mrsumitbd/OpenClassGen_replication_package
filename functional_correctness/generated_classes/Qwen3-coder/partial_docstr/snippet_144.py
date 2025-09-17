class Pipe(object):
    '''An object representing a pipe-able callable, optionally with preserved arguments.

    Using this you can construct custom subclasses (define a method named "callable") or use it as a decorator:

            @Pipe
            def s(text):
                    return str(text)

    '''

    def __init__(self, callable, *args, **kw):
        self._callable = callable
        self._args = args
        self._kw = kw

    def __repr__(self):
        return f'<Pipe {self._callable.__name__}>'

    def __ror__(self, other):
        '''The main machinery of the Pipe, calling the chosen callable with the recorded arguments.'''
        return self._callable(other, *self._args, **self._kw)

    def __call__(self, *args, **kw):
        '''Allow for the preserved args and kwargs to be updated, returning a mutated copy.

        This allows for usage with arguments, as in the following example:

                "Hello!" | encode('utf8')

        This also allows for easy construction of custom mutated copies for use later, a la:

                utf8 = encode('utf8')
                "Hello!" | utf8
        '''
        return Pipe(self._callable, *args, **kw)