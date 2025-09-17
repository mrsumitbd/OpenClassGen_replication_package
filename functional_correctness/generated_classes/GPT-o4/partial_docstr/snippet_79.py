class Memoize(object):
    '''A general memoization class, specify a function when creating a new
    instance of the class. The functions return value is returned and stored in
    ``self.memo`` when the instance is called with an argument for the first
    time. Later calls with the same argument return the cached value, instead of
    calling the function again.

    :ivar function: when ``Memoize`` is called this functions return value is
        returned.
    :ivar memo: a dictionary that records the ``function`` return values of
        already called variables.
    '''

    def __init__(self, function):
        self.function = function
        self.memo = {}

    def __call__(self, arg):
        if arg not in self.memo:
            self.memo[arg] = self.function(arg)
        return self.memo[arg]