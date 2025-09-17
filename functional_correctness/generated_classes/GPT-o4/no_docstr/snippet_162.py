class RmcpMsg(object):
    RMCP_VERSION = 0x06
    RMCP_RESERVED = 0x00
    HEADER_LEN = 4

    def __init__(self, class_of_msg=None):
        self.version = self.RMCP_VERSION
        self.reserved = self.RMCP_RESERVED
        self.class_of_msg = class_of_msg if class_of_msg is not None else 0x07
        self.seq_number = None
        self.sdu = None

    def pack(self, sdu, seq_number):
        if not isinstance(sdu, (bytes, bytearray)):
            raise TypeError("SDU must be bytes or bytearray")
        if not (0 <= seq_number <= 0xFF):
            raise ValueError("Sequence number must be in 0..255")
        hdr = struct.pack('!BBBB', self.version, self.reserved, seq_number, self.class_of_msg)
        return hdr + sdu

    def unpack(self, pdu):
        if not isinstance(pdu, (bytes, bytearray)):
            raise TypeError("PDU must be bytes or bytearray")
        if len(pdu) < self.HEADER_LEN:
            raise ValueError("PDU too short for RMCP header")
        self.version, self.reserved, self.seq_number, self.class_of_msg = struct.unpack('!BBBB', pdu[:4])
        self.sdu = pdu[4:]
        return self.sdu