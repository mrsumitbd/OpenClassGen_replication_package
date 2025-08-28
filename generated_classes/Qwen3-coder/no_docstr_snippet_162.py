class RmcpMsg(object):
    def __init__(self, class_of_msg=None):
        self.class_of_msg = class_of_msg
        self.version = 0x06
        self.reserved = 0x00
        self.seq_number = 0
        self.sdu = b''

    def pack(self, sdu, seq_number):
        self.sdu = sdu
        self.seq_number = seq_number
        
        # RMCP header: version, reserved, seq_number, class
        header = bytes([
            self.version,
            self.reserved,
            self.seq_number & 0xFF,
            self.class_of_msg if self.class_of_msg is not None else 0x00
        ])
        
        # Combine header and SDU
        pdu = header + self.sdu
        return pdu

    def unpack(self, pdu):
        if len(pdu) < 4:
            raise ValueError("PDU too short to contain RMCP header")
        
        # Extract header fields
        self.version = pdu[0]
        self.reserved = pdu[1]
        self.seq_number = pdu[2]
        self.class_of_msg = pdu[3]
        
        # Extract SDU (payload)
        self.sdu = pdu[4:]
        
        return self.sdu, self.seq_number