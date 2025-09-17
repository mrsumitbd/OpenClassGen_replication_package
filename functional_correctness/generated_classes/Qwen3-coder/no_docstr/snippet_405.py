class Event(object):
    def __init__(self, start_mark=None, end_mark=None):
        self.start_mark = start_mark
        self.end_mark = end_mark

    def __repr__(self):
        return f"{self.__class__.__name__}(start_mark={self.start_mark!r}, end_mark={self.end_mark!r})"