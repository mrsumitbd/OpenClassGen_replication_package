class Incrementer:
    def __init__(self, start=0):
        self.value = start
        self.increment = 1

    def __iter__(self):
        return self

    def __next__(self):
        current = self.value
        self.value += self.increment
        return current

    def send(self, val):
        if val is not None:
            self.increment = val
        return self.__next__()