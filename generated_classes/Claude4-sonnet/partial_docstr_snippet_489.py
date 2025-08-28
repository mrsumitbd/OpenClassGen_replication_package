class Renderable:
    '''A render-able (color or style) named object'''

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __call__(self, text, size=None):
        '''
        Allows for convenient call of the form:

        >>> import runez
        >>> runez.blue("foo")
        'foo'
        '''
        return self.rendered(text)

    def rendered(self, text):
        return str(text)