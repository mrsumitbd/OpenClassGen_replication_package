class Incrementer:
    def __init__(self):
        self._value = 0
        self._waiting = None
        self._first = True

    def __iter__(self):
        return self

    def __next__(self):
        if self._waiting is not None:
            self._value = self._waiting
            self._waiting = None
        else:
            if not self._first:
                self._value += 1
        self._first = False
        return self._value

    def send(self, val):
        self._waiting = val
        return self.__next__()