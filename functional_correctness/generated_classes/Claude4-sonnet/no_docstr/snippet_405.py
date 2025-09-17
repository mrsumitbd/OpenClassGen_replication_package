class Event(object):

    def __init__(self, start_mark=None, end_mark=None):
        self.start_mark = start_mark
        self.end_mark = end_mark

    def __repr__(self):
        attributes = [key for key, value in self.__dict__.items()
                     if not key.endswith('_mark')]
        attributes.sort()
        arguments = ', '.join(['%s=%r' % (key, getattr(self, key))
                              for key in attributes])
        if arguments:
            return '%s(%s)' % (self.__class__.__name__, arguments)
        else:
            return '%s()' % self.__class__.__name__