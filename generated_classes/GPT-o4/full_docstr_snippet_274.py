class Array:
    """Use a Struct as a callable to unpack a bunch of bytes as a list."""

    def __init__(self, fmt):
        """Initialize the Struct unpacker."""
        self.struct = struct.Struct(fmt)
        self.size = self.struct.size

    def __call__(self, buf):
        """Perform the actual unpacking."""
        length = len(buf)
        if length % self.size:
            raise ValueError("Buffer length must be a multiple of struct size")
        count = length // self.size
        return [self.struct.unpack_from(buf, i * self.size) for i in range(count)]