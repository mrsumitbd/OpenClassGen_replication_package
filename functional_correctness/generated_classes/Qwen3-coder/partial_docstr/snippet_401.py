class Peekable:
    '''
    Wrapper for a traditional iterable to give it a peek attribute.

    >>> nums = Peekable(range(2))
    >>> nums.peek()
    0
    >>> nums.peek()
    0
    >>> next(nums)
    0
    >>> nums.peek()
    1
    >>> next(nums)
    1
    >>> nums.peek()
    Traceback (most recent call last):
    ...
    StopIteration

    Peekable should accept an iterable and not just an iterator.

    >>> list(Peekable(range(2)))
    [0, 1]
    '''

    def __new__(cls, iterator):
        return super().__new__(cls)

    def __init__(self, iterator):
        self.iterator = iter(iterator)
        self._peeked = None
        self._has_peeked = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._has_peeked:
            self._has_peeked = False
            return self._peeked
        return next(self.iterator)

    def peek(self):
        if not self._has_peeked:
            self._peeked = next(self.iterator)
            self._has_peeked = True
        return self._peeked