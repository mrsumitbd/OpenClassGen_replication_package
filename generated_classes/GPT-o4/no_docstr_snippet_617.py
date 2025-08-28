class BinLine:
    def __init__(self, row):
        # Accept a string like "1010" or an iterable of 0/1 ints
        try:
            self.bits = [int(x) for x in row]
        except Exception:
            raise ValueError("Row must be iterable of 0/1")
        for b in self.bits:
            if b not in (0, 1):
                raise ValueError("Elements must be 0 or 1")

    def __str__(self):
        return ''.join(str(b) for b in self.bits)

    def subtract(self, o):
        if not isinstance(o, BinLine):
            raise TypeError("Operand must be a BinLine")
        if len(self.bits) != len(o.bits):
            raise ValueError("Lengths must match")
        result = [(a ^ b) for a, b in zip(self.bits, o.bits)]
        return BinLine(result)