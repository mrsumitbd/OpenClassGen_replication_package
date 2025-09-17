class Incrementer:
    def __init__(self, start=0, step=1):
        self.start = start
        self.step = step
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        value = self.current
        self.current += self.step
        return value

    def send(self, val):
        if val is not None:
            self.current = val
        value = self.current
        self.current += self.step
        return value