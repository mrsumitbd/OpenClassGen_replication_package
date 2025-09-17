class EnumValueGenerator:
    def __init__(self, start=1):
        self.start = start
        self.current = start

    def reset(self, start=1):
        self.start = start
        self.current = start

    def next(self):
        value = self.current
        self.current += 1
        return value

    def __call__(self):
        return self.next()

    def __repr__(self):
        return f"EnumValueGenerator(start={self.start}, current={self.current})"