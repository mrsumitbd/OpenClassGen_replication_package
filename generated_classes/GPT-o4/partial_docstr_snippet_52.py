class DefaultStringType(object):
    '''
    Decorator that uses the default version (A or W) to call
    based on the configuration of the L{GuessStringType} decorator.

    @see: L{GuessStringType.t_default}

    @type fn_ansi: function
    @ivar fn_ansi: ANSI version of the API function to call.
    @type fn_unicode: function
    @ivar fn_unicode: Unicode (wide) version of the API function to call.
    '''
    def __init__(self, fn_ansi, fn_unicode):
        '''
        @type  fn_ansi: function
        @param fn_ansi: ANSI version of the API function to call.
        @type  fn_unicode: function
        @param fn_unicode: Unicode (wide) version of the API function to call.
        '''
        self.fn_ansi = fn_ansi
        self.fn_unicode = fn_unicode
        update_wrapper(self, fn_ansi)

    def __call__(self, *argv, **argd):
        from __main__ import GuessStringType
        t = GuessStringType.t_default
        if t == 'W':
            return self.fn_unicode(*argv, **argd)
        return self.fn_ansi(*argv, **argd)