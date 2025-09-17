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
        self.newcardonly = bool(newcardonly)
        self._requested_readers = readers[:] if readers is not None else None
        self.cardType = cardType or AnyCardType()
        self.cardServiceClass = cardServiceClass or PassThruCardService
        self.timeout = timeout

        # Track initial card presence per reader (for newcardonly)
        self._initial_atrs = {}
        if self.newcardonly:
            for rdr in self.getReaders():
                try:
                    con = rdr.createConnection()
                    con.connect()
                    atr = tuple(con.getATR())
                    self._initial_atrs[rdr.name] = atr
                    con.disconnect()
                except Exception:
                    pass

        # Track reader insertion state for waitforcardevent
        self._reader_states = {}
        for rdr in self.getReaders():
            try:
                con = rdr.createConnection()
                con.connect()
                self._reader_states[rdr.name] = True
                con.disconnect()
            except Exception:
                self._reader_states[rdr.name] = False

    def getReaders(self):
        '''Returns the list or readers on which to wait for cards.'''
        all_rdrs = _get_readers()
        if not all_rdrs:
            raise NoReadersException("No smartcard readers available")
        if self._requested_readers is None:
            return all_rdrs
        selected = []
        names = set(self._requested_readers)
        for rdr in all_rdrs:
            if rdr.name in names:
                selected.append(rdr)
        if not selected:
            raise NoReadersException(
                "No readers matching %r found" % (self._requested_readers,)
            )
        return selected

    def waitforcard(self):
        '''Wait for card insertion and returns a card service.'''
        deadline = None
        if self.timeout is not None:
            deadline = time.time() + float(self.timeout)
        while True:
            if deadline is not None and time.time() > deadline:
                raise CardRequestTimeoutException("Timeout waiting for card")
            for rdr in self.getReaders():
                try:
                    con = rdr.createConnection()
                    con.connect()
                    atr = tuple(con.getATR())
                except Exception:
                    continue
                # ATR must match requested cardType
                if not self.cardType.match(atr):
                    try:
                        con.disconnect()
                    except Exception:
                        pass
                    continue
                # If newcardonly, skip cards present at init
                if self.newcardonly:
                    init = self._initial_atrs.get(rdr.name)
                    if init is not None and init == atr:
                        try:
                            con.disconnect()
                        except Exception:
                            pass
                        continue
                # success: bind and return
                return self.cardServiceClass(con)
            time.sleep(0.1)

    def waitforcardevent(self):
        '''Wait for card insertion or removal.'''
        deadline = None
        if self.timeout is not None:
            deadline = time.time() + float(self.timeout)
        while True:
            if deadline is not None and time.time() > deadline:
                raise CardRequestTimeoutException("Timeout waiting for card event")
            for rdr in self.getReaders():
                name = rdr.name
                old_state = self._reader_states.get(name, False)
                new_state = False
                try:
                    con = rdr.createConnection()
                    con.connect()
                    new_state = True
                    con.disconnect()
                except Exception:
                    new_state = False
                if new_state != old_state:
                    self._reader_states[name] = new_state
                    return (rdr, new_state)
            time.sleep(0.1)