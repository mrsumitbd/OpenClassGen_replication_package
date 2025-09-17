class BitStream:
    '''Represent a bytes object. Can read bits and prefix codes the way
    Brotli does.
    '''

    def __init__(self, byteString):
        self.data = byteString
        self.byte_pos = 0
        self.bit_pos = 0

    def __repr__(self):
        '''Representation
        >>> olleke
        BitStream(pos=0:0)
        '''
        return f"BitStream(pos={self.byte_pos}:{self.bit_pos})"

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
        result = 0
        bits_read = 0
        
        while bits_read < n:
            if self.byte_pos >= len(self.data):
                break
                
            current_byte = self.data[self.byte_pos]
            bits_available_in_byte = 8 - self.bit_pos
            bits_needed = n - bits_read
            bits_to_read = min(bits_available_in_byte, bits_needed)
            
            mask = (1 << bits_to_read) - 1
            bits = (current_byte >> self.bit_pos) & mask
            result |= bits << bits_read
            
            bits_read += bits_to_read
            self.bit_pos += bits_to_read
            
            if self.bit_pos >= 8:
                self.bit_pos = 0
                self.byte_pos += 1
                
        return result

    def peek(self, n):
        '''Peek an n bit integer from the stream without updating the pointer.
        It is not an error to read beyond the end of the stream.
        >>> olleke.data[:2]==b'.' and 0x2e1b==11803
        True
        >>> olleke.peek(15)
        11803
        >>> hex(olleke.peek(32))
        '0x2e1b'
        '''
        saved_byte_pos = self.byte_pos
        saved_bit_pos = self.bit_pos
        result = self.read(n)
        self.byte_pos = saved_byte_pos
        self.bit_pos = saved_bit_pos
        return result

    def readBytes(self, n):
        '''Read n bytes from the stream on a byte boundary.
        '''
        if self.bit_pos != 0:
            self.bit_pos = 0
            self.byte_pos += 1
            
        result = self.data[self.byte_pos:self.byte_pos + n]
        self.byte_pos += n
        return result