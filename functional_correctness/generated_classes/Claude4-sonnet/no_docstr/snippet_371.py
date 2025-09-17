class TryExcept(object):

    def __init__(self, try_, except_):
        self.try_ = try_
        self.except_ = except_

    def generate(self):
        try_code = self.try_.generate() if hasattr(self.try_, 'generate') else str(self.try_)
        except_code = self.except_.generate() if hasattr(self.except_, 'generate') else str(self.except_)
        
        return f"try:\n    {try_code}\nexcept:\n    {except_code}"