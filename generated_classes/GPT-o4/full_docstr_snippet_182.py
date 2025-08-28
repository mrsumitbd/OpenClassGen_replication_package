class Session:
    '''The Session object enables programmers to transmit APDU to smartcards.

    This is an example of use of the Session object:

    >>> import smartcard
    >>> reader=smartcard.listReaders()
    >>> s = smartcard.Session(reader[0])
    >>> SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
    >>> DF_TELECOM = [0x7F, 0x10]
    >>> data, sw1, sw2 = s.sendCommandAPDU(SELECT+DF_TELECOM)
    >>> print(data, sw1, sw2)
    >>> s.close()
    >>> print(`s`)
    '''

    def __init__(self, readerName=None, cardServiceClass=None):
        '''Session constructor. Initializes a smart card session and
           connect to the card.

           @param readerName: reader to connect to; default is first PCSC reader
           @param cardServiceClass: card service to bind the session to; default
                                    is None
        '''
        rdrs = readers()
        if not rdrs:
            raise NoReadersException("No PC/SC readers found")
        # select reader
        if readerName is None:
            self.reader = rdrs[0]
        else:
            # if user passed a Reader instance
            if readerName in rdrs:
                self.reader = readerName
            else:
                # try matching by name
                match = [r for r in rdrs if str(r) == str(readerName)]
                if match:
                    self.reader = match[0]
                else:
                    raise ValueError("Reader %r not found" % readerName)
        # create connection
        self.connection = self.reader.createConnection()
        try:
            self.connection.connect()
        except CardConnectionException as e:
            raise CardConnectionException("Failed to connect to card: %s" % e)
        # store ATR
        try:
            self._atr = self.connection.getATR()
        except Exception:
            self._atr = None
        self._connected = True

    def close(self):
        '''Close the smartcard session.

           Closing a session will disconnect from the card.'''
        if self._connected:
            try:
                self.connection.disconnect()
            except Exception:
                pass
            self._connected = False

    def sendCommandAPDU(self, command):
        '''Send an APDU command to the connected smartcard.

           @param command: list of APDU bytes, e.g. [0xA0, 0xA4, 0x00, 0x00, 0x02]

           @return: a tuple (response, sw1, sw2) where
                   response is the APDU response
                   sw1, sw2 are the two status words
        '''
        if not self._connected:
            raise CardConnectionException("Session is closed")
        resp = self.connection.transmit(command)
        # pyscard may return (data, sw1, sw2) or a flat list
        if isinstance(resp, tuple) and len(resp) == 3:
            return resp
        # flat list
        if isinstance(resp, list) and len(resp) >= 2:
            sw1, sw2 = resp[-2], resp[-1]
            data = resp[:-2]
            return data, sw1, sw2
        raise RuntimeError("Unexpected response format: %r" % resp)

    def getATR(self):
        '''Returns the ATR of the connected card.'''
        return self._atr

    def __repr__(self):
        '''Returns a string representation of the session.'''
        status = "connected" if self._connected else "closed"
        reader_name = str(self.reader)
        atr = self._atr or []
        return "<Session reader=%r ATR=%s status=%s>" % (reader_name, atr, status)