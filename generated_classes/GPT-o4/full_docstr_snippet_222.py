class SomeClass:
    '''cds'''

    def __init__(self):
        '''only to make pylint happier'''
        self._silent = False

    def please(self):
        '''public method 1/2'''
        if not self._silent:
            print('Please?')

    def besilent(self):
        '''public method 2/2'''
        self._silent = True