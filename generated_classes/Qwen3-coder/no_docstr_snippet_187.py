class Query_Field(object):
    def __init__(self, name, is_neg=False):
        self.name = name
        self.is_neg = is_neg

    def __neg__(self):
        return Query_Field(self.name, not self.is_neg)