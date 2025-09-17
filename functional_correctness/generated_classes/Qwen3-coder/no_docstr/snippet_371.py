class TryExcept(object):
    def __init__(self, try_, except_):
        self.try_ = try_
        self.except_ = except_

    def generate(self):
        return f"try:\n{self.try_}\nexcept:\n{self.except_}"