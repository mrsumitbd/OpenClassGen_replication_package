class _NotSet(object):

    def __nonzero__(self):
        return False

    def __repr__(self):
        return '_NotSet()'

    def __str__(self):
        return 'NotSet'

    def __eq__(self, other):
        return isinstance(other, _NotSet)