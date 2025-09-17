class Event(object):
    def __init__(self, start_mark=None, end_mark=None):
        self.start_mark = start_mark
        self.end_mark = end_mark

    def __repr__(self):
        return "{}(start_mark={!r}, end_mark={!r})".format(
            self.__class__.__name__, self.start_mark, self.end_mark
        )