class EnumValueGenerator:
    def __init__(self, start=1):
        self.start = start
        self.current = start - 1

    def reset(self, start=1):
        self.start = start
        self.current = start - 1

    def next(self):
        self.current += 1
        return self.current

    def __call__(self):
        return self.next()

    def __repr__(self):
        return f"{self.__class__.__name__}(start={self.start}, next={self.current + 1})"