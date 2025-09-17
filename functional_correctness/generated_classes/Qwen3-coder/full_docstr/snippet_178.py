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
        self.chain = chain
        self.strategy = strategy
        self.filterExceptions = []

    def next(self):
        '''Returns next error checking strategy.'''
        return self.chain

    def addFilterException(self, exClass):
        '''Add an exception filter to the error checking chain.

        @param exClass:    the exception to exclude, e.g.
        L{smartcard.sw.SWExceptions.WarningProcessingException} A filtered
        exception will not be raised when the sw1,sw2 conditions that
        would raise the exception are met.
        '''
        self.filterExceptions.append(exClass)

    def end(self):
        '''Returns True if this is the end of the error checking
        strategy chain.'''
        return self.chain is None

    def __call__(self, data, sw1, sw2):
        '''Called to test data, sw1 and sw2 for error on the chain.'''
        try:
            # Apply the current strategy
            self.strategy(data, sw1, sw2)
        except Exception as e:
            # Check if the exception is filtered
            for exClass in self.filterExceptions:
                if isinstance(e, exClass):
                    # If filtered, don't raise and continue to next chain
                    if not self.end():
                        return self.next()(data, sw1, sw2)
                    return
            # If not filtered, re-raise the exception
            raise
        
        # If no exception from current strategy, continue to next chain
        if not self.end():
            return self.next()(data, sw1, sw2)