class TimeSinceLastTransaction(object):
    def __init__(self, seconds):
        if not isinstance(seconds, (int, float)):
            raise TypeError(f"seconds must be int or float, not {type(seconds).__name__}")
        if seconds < 0:
            raise ValueError("seconds must be non-negative")
        self._seconds = seconds

    @property
    def seconds(self):
        return self._seconds

    def __eq__(self, other):
        if not isinstance(other, TimeSinceLastTransaction):
            return NotImplemented
        return self.seconds == other.seconds

    def __repr__(self):
        return f"TimeSinceLastTransaction(seconds={self.seconds!r})"