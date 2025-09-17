class ExtensionPCTS14:

    @staticmethod
    def decode_extra(packet, bbuff):
        if len(bbuff) < 4:
            return False
        
        packet.picture_id = int.from_bytes(bbuff[:2], byteorder='big')
        packet.temporal_layer_zero_index = int.from_bytes(bbuff[2:4], byteorder='big')
        
        return True

    @staticmethod
    def encode_extra(packet):
        if not hasattr(packet, 'picture_id') or not hasattr(packet, 'temporal_layer_zero_index'):
            return b''
        
        extra_data = packet.picture_id.to_bytes(2, byteorder='big')
        extra_data += packet.temporal_layer_zero_index.to_bytes(2, byteorder='big')
        
        return extra_data