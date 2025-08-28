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

    DEFAULT_PROTOCOL_VERSION = 100
    DEFAULT_HEADER_SIZE = 24

    def __init__(self, protocol_version=None, header_size=None):
        '''
            @type protocol_version: int or None
            @type header_size: int or None
        '''
        if protocol_version is None:
            protocol_version = self.DEFAULT_PROTOCOL_VERSION
        if header_size is None:
            header_size = self.DEFAULT_HEADER_SIZE
        self.protocol_version = protocol_version
        self.header_size = header_size

    def validate(self):
        '''Checks whether this OmapiStartupMessage matches the implementation.
            @raises OmapiError:
        '''
        if (self.protocol_version != self.DEFAULT_PROTOCOL_VERSION or
            self.header_size != self.DEFAULT_HEADER_SIZE):
            raise OmapiError("protocol mismatch")

    def as_string(self):
        '''
            @rtype: bytes
        '''
        return struct.pack(">II",
                           self.protocol_version,
                           self.header_size)

    def serialize(self, outbuffer):
        '''Serialize this OmapiStartupMessage to the given outbuffer.
            @type outbuffer: OutBuffer
        '''
        outbuffer.write(self.as_string())

    def dump_oneline(self):
        '''
            @rtype: str
            @returns: a human readable representation in one line
        '''
        return ("OmapiStartupMessage(protocol_version=%d, "
                "header_size=%d)") % (
                    self.protocol_version,
                    self.header_size)