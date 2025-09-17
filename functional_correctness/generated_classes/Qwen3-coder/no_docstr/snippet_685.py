class ExtensionPCTS14:
    @staticmethod
    def decode_extra(packet, bbuff):
        # Extract the extra data length from the packet
        extra_len = packet.get('extra_len', 0)
        
        # If there's no extra data, return early
        if extra_len == 0:
            return
        
        # Read the extra data from the byte buffer
        extra_data = bbuff.read(extra_len)
        
        # Store the extra data in the packet
        packet['extra_data'] = extra_data

    @staticmethod
    def encode_extra(packet):
        # Get the extra data from the packet
        extra_data = packet.get('extra_data', b'')
        
        # Set the extra data length in the packet
        packet['extra_len'] = len(extra_data)
        
        # Return the extra data to be written to the byte buffer
        return extra_data