class ReverseComparator:
    '''
    Object which swaps '<' and '>' so
    instead of a < b, it does b < a,
    and instead of a > b, it does b > a.
    This can be used in reverse comparisons.
    '''

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        other_val = other.value if isinstance(other, ReverseComparator) else other
        return other_val < self.value

    def __eq__(self, other):
        other_val = other.value if isinstance(other, ReverseComparator) else other
        return self.value == other_val

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        other_val = other.value if isinstance(other, ReverseComparator) else other
        return other_val > self.value