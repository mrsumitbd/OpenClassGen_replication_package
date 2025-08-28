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
        from smartcard.System import readers
        from smartcard.CardService import CardService
        from smartcard.CardConnection import CardConnection
        
        if readerName is None:
            reader_list = readers()
            if not reader_list:
                raise Exception("No smart card readers available")
            self.reader = reader_list[0]
        else:
            self.reader = readerName
            
        self.cardServiceClass = cardServiceClass
        self.connection = self.reader.createConnection()
        self.connection.connect()
        self.closed = False

    def close(self):
        '''Close the smartcard session.

        Closing a session will disconnect from the card.'''
        if not self.closed:
            self.connection.disconnect()
            self.closed = True

    def sendCommandAPDU(self, command):
        '''Send an APDU command to the connected smartcard.

        @param command: list of APDU bytes, e.g. [0xA0, 0xA4, 0x00, 0x00, 0x02]

        @return: a tuple (response, sw1, sw2) where
                response is the APDU response
                sw1, sw2 are the two status words
        '''
        if self.closed:
            raise Exception("Session is closed")
        
        response, sw1, sw2 = self.connection.transmit(command)
        return response, sw1, sw2

    def getATR(self):
        '''Returns the ATR of the connected card.'''
        if self.closed:
            raise Exception("Session is closed")
        
        return self.connection.getATR()

    def __repr__(self):
        '''Returns a string representation of the session.'''
        if self.closed:
            return f"<Session: closed>"
        else:
            return f"<Session: {self.reader.name}>"