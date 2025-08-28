class Py3Cmp:
    def __init__(self, obj, *args):
        self.obj = obj

    def __eq__(self, other):
        return self.obj == other.obj

    def __ne__(self, other):
        return self.obj != other.obj

    def __gt__(self, other):
        return self.obj > other.obj

    def __lt__(self, other):
        return self.obj < other.obj

    def __ge__(self, other):
        return self.obj >= other.obj

    def __le__(self, other):
        return self.obj <= other.obj