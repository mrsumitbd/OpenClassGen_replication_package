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
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value < other.value