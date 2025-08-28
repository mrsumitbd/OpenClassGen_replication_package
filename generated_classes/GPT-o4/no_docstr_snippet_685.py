class ExtensionPCTS14:
    @staticmethod
    def decode_extra(packet, bbuff):
        # read all remaining bytes as the extension’s payload
        packet.extra = bbuff.read()

    @staticmethod
    def encode_extra(packet):
        # return the stored payload (or empty if none)
        return getattr(packet, 'extra', b'')