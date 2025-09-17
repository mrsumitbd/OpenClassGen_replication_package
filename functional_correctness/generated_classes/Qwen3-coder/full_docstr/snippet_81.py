class OmapiStartupMessage(object):
    '''Class describing the protocol negotiation messages.

    >>> s = OmapiStartupMessage().as_string()
    >>> s == b"\0\0\0\x64\0\0\0\x18"
    True
    >>> next(InBuffer(s).parse_startup_message()).validate()
    >>> OmapiStartupMessage(42).validate()
    Traceback (most recent call last):
    ...
    OmapiError: protocol mismatch
    '''

    def __init__(self, protocol_version=None, header_size=None):
        '''
        @type protocol_version: int or None
        @type header_size: int or None
        '''
        if protocol_version is None:
            protocol_version = 100
        if header_size is None:
            header_size = 24
        self.protocol_version = protocol_version
        self.header_size = header_size

    def validate(self):
        '''Checks whether this OmapiStartupMessage matches the implementation.
        @raises OmapiError:
        '''
        if self.protocol_version != 100 or self.header_size != 24:
            raise OmapiError("protocol mismatch")

    def as_string(self):
        '''
        @rtype: bytes
        '''
        outbuffer = OutBuffer()
        self.serialize(outbuffer)
        return outbuffer.getvalue()

    def serialize(self, outbuffer):
        '''Serialize this OmapiStartupMessage to the given outbuffer.
        @type outbuffer: OutBuffer
        '''
        outbuffer.add_net32int(self.protocol_version)
        outbuffer.add_net32int(self.header_size)

    def dump_oneline(self):
        '''
        @rtype: str
        @returns: a human readable representation in one line
        '''
        return f"OmapiStartupMessage(protocol_version={self.protocol_version}, header_size={self.header_size})"