class ErrorCheckingChain:
    '''The error checking chain is a list of response apdu status word
    (sw1, sw2) error check strategies. Each strategy in the chain is
    called until an error is detected. A L{smartcard.sw.SWExceptions}
    exception is raised when an error is detected. No exception is
    raised if no error is detected.

    Implementation derived from Bruce Eckel, Thinking in Python. The
    L{ErrorCheckingChain} implements the Chain Of Responsibility design
    pattern.
    '''

    def __init__(self, chain, strategy):
        '''constructor. Appends a strategy to the L{ErrorCheckingChain}
           chain.'''
        if chain is None:
            self._filters = []
        else:
            self._filters = chain._filters
        self._chain = chain
        self._strategy = strategy

    def next(self):
        '''Returns next error checking strategy.'''
        return self._chain

    def addFilterException(self, exClass):
        '''Add an exception filter to the error checking chain.

        @param exClass:    the exception to exclude, e.g.
        L{smartcard.sw.SWExceptions.WarningProcessingException} A filtered
        exception will not be raised when the sw1,sw2 conditions that
        would raise the exception are met.
        '''
        self._filters.append(exClass)

    def end(self):
        '''Returns True if this is the end of the error checking
        strategy chain.'''
        return self._chain is None

    def __call__(self, data, sw1, sw2):
        '''Called to test data, sw1 and sw2 for error on the chain.'''
        try:
            if self._strategy:
                self._strategy(data, sw1, sw2)
        except Exception as ex:
            for filt in self._filters:
                if isinstance(ex, filt):
                    if self._chain:
                        return self._chain(data, sw1, sw2)
                    return
            raise
        else:
            if self._chain:
                return self._chain(data, sw1, sw2)