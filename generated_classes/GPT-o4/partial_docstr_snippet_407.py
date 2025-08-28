class BitStream:
    '''Represent a bytes object. Can read bits and prefix codes the way
    Brotli does.
    '''

    def __init__(self, byteString):
        self.data = byteString
        self.pos = 0

    def __repr__(self):
        return f"BitStream(pos={self.pos//8}:{self.pos%8})"

    def read(self, n):
        val = self.peek(n)
        self.pos += n
        return val

    def peek(self, n):
        if n <= 0:
            return 0
        byte_index = self.pos // 8
        bit_index = self.pos % 8
        bits_needed = bit_index + n
        num_bytes = (bits_needed + 7) // 8
        raw = self.data[byte_index:byte_index + num_bytes]
        raw_int = int.from_bytes(raw, 'little')
        return (raw_int >> bit_index) & ((1 << n) - 1)

    def readBytes(self, n):
        if self.pos % 8 != 0:
            raise ValueError("Position not at byte boundary")
        byte_index = self.pos // 8
        chunk = self.data[byte_index:byte_index + n]
        if len(chunk) < n:
            chunk += b'\x00' * (n - len(chunk))
        self.pos += 8 * n
        return chunk