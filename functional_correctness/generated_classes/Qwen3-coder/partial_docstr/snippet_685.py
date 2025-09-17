class Splitter:
    '''object that will split a string with the given arguments for each call

    >>> s = Splitter(',')
    >>> s('hello, world, this is your, master calling')
    ['hello', ' world', ' this is your', ' master calling']
    '''

    def __init__(self, *args):
        self.args = args

    def __call__(self, s):
        return s.split(*self.args)