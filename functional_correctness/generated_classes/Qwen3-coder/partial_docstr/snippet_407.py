class BitStream:
    '''Represent a bytes object. Can read bits and prefix codes the way
    Brotli does.
    '''

    def __init__(self, byteString):
        self.data = byteString
        self.pos = 0  # bit position as (byte_index, bit_offset)

    def __repr__(self):
        '''Representation
        >>> olleke
        BitStream(pos=0:0)
        '''
        byte_pos, bit_offset = divmod(self.pos, 8)
        return f"BitStream(pos={byte_pos}:{bit_offset})"

    def read(self, n):
        '''Read n bits from the stream and return as an integer.
        Produces zero bits beyond the stream.
        >>> olleke.data[0]==27
        True
        >>> olleke.read(5)
        27

        >>> olleke
        BitStream(pos=0:5)
        '''
        result = self.peek(n)
        self.pos += n
        return result

    def peek(self, n):
        '''Peek an n bit integer from the stream without updating the pointer.
        It is not an error to read beyond the end of the stream.
        >>> olleke.data[:2]==b'.' and 0x2e1b==11803
        True
        >>> olleke.peek(15)
        11803
        >>> hex(olleke.peek(32))
        '0x2e1b'
        '''
        if n == 0:
            return 0
            
        byte_index, bit_offset = divmod(self.pos, 8)
        result = 0
        
        bits_read = 0
        current_byte_index = byte_index
        
        while bits_read < n:
            if current_byte_index >= len(self.data):
                # Beyond the stream, return zero bits
                bits_read += 1
                result <<= 1
                continue
                
            # Get the current byte
            current_byte = self.data[current_byte_index]
            
            # Calculate how many bits we can read from this byte
            bits_available_in_byte = 8 - bit_offset if current_byte_index == byte_index else 8
            bits_to_read_from_byte = min(n - bits_read, bits_available_in_byte)
            
            if current_byte_index == byte_index:
                # First byte: need to account for bit_offset
                mask = (1 << (8 - bit_offset)) - 1  # mask for remaining bits
                bits = (current_byte & mask) >> (8 - bit_offset - bits_to_read_from_byte)
            else:
                # Subsequent bytes: read from the beginning
                bits = current_byte >> (8 - bits_to_read_from_byte)
            
            # Add these bits to result
            result = (result << bits_to_read_from_byte) | bits
            
            bits_read += bits_to_read_from_byte
            
            # Update for next iteration
            if current_byte_index == byte_index:
                bit_offset += bits_to_read_from_byte
                if bit_offset >= 8:
                    current_byte_index += 1
                    bit_offset = 0
            else:
                current_byte_index += 1
        
        return result

    def readBytes(self, n):
        '''Read n bytes from the stream on a byte boundary.
        '''
        # Align to byte boundary
        byte_pos, bit_offset = divmod(self.pos, 8)
        if bit_offset > 0:
            byte_pos += 1
            bit_offset = 0
        
        # Update position to byte boundary
        self.pos = byte_pos * 8
        
        # Read n bytes
        result = self.data[byte_pos:byte_pos + n]
        
        # Update position
        self.pos += n * 8
        
        return result