class TimeSinceLastTransaction(object):
    def __init__(self, seconds):
        self._seconds = seconds

    @property
    def seconds(self):
        return self._seconds

    def __eq__(self, other):
        if not isinstance(other, TimeSinceLastTransaction):
            return False
        return self._seconds == other._seconds

    def __repr__(self):
        return f"TimeSinceLastTransaction({self._seconds})"