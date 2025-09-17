class AbstractCardRequest:
    '''The base class for xxxCardRequest classes.

    A CardRequest is used for waitForCard() invocations and specifies what
    kind of smart card an application is waited for.'''

    def __init__(
        self,
        newcardonly=False,
        readers=None,
        cardType=None,
        cardServiceClass=None,
        timeout=1,
    ):
        '''Construct new CardRequest.

        @param newcardonly: if True, request a new card; default is
                            False, i.e. accepts cards already inserted

        @param readers:     the list of readers to consider for
                            requesting a card; default is to consider
                            all readers

        @param cardType:    the L{smartcard.CardType.CardType} to wait for;
                            default is L{smartcard.CardType.AnyCardType},
                            i.e. the request will succeed with any card

        @param cardServiceClass: the specific card service class to create
                            and bind to the card;default is to create
                            and bind a L{smartcard.PassThruCardService}

        @param timeout:     the time in seconds we are ready to wait for
                            connecting to the requested card.  default
                            is to wait one second; to wait forever, set
                            timeout to None
        '''
        self.newcardonly = newcardonly
        self.readers = readers
        self.cardType = cardType
        self.cardServiceClass = cardServiceClass
        self.timeout = timeout

    def getReaders(self):
        '''Returns the list or readers on which to wait for cards.'''
        return self.readers

    def waitforcard(self):
        '''Wait for card insertion and returns a card service.'''
        raise NotImplementedError("waitforcard method must be implemented in subclass")

    def waitforcardevent(self):
        '''Wait for card insertion or removal.'''
        raise NotImplementedError("waitforcardevent method must be implemented in subclass")