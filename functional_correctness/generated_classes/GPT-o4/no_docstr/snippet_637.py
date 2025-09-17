class Py3Cmp:
    def __eq__(self, other):
        try:
            r = self.cmp(other)
        except Exception:
            return NotImplemented
        return r == 0

    def __ne__(self, other):
        try:
            r = self.cmp(other)
        except Exception:
            return NotImplemented
        return r != 0

    def __lt__(self, other):
        try:
            r = self.cmp(other)
        except Exception:
            return NotImplemented
        return r < 0

    def __le__(self, other):
        try:
            r = self.cmp(other)
        except Exception:
            return NotImplemented
        return r <= 0

    def __gt__(self, other):
        try:
            r = self.cmp(other)
        except Exception:
            return NotImplemented
        return r > 0

    def __ge__(self, other):
        try:
            r = self.cmp(other)
        except Exception:
            return NotImplemented
        return r >= 0