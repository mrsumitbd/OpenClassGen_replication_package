class WIC_1T(object):
    '''
    WIC-1T Serial
    '''

    def __init__(self):
        self._interfaces = 1

    def __str__(self):
        return "WIC-1T Serial"

    @property
    def interfaces(self):
        '''
        Returns the number of interfaces supported by this WIC.

        :returns: number of interfaces
        '''
        return self._interfaces