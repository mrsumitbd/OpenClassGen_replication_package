class RmcpMsg(object):

    def __init__(self, class_of_msg=None):
        self.version = 0x06
        self.reserved = 0x00
        self.sequence_number = 0x00
        self.class_of_msg = class_of_msg if class_of_msg is not None else 0x07
        self.data = b''

    def pack(self, sdu, seq_number):
        self.data = sdu
        self.sequence_number = seq_number & 0xFF
        data_length = len(sdu)
        
        header = struct.pack('!BBBB', 
                           self.version,
                           self.reserved, 
                           self.sequence_number,
                           self.class_of_msg)
        
        pdu = header + sdu
        return pdu

    def unpack(self, pdu):
        if len(pdu) < 4:
            raise ValueError("PDU too short")
        
        header = pdu[:4]
        self.version, self.reserved, self.sequence_number, self.class_of_msg = struct.unpack('!BBBB', header)
        
        self.data = pdu[4:]
        
        return {
            'version': self.version,
            'reserved': self.reserved,
            'sequence_number': self.sequence_number,
            'class_of_msg': self.class_of_msg,
            'data': self.data
        }