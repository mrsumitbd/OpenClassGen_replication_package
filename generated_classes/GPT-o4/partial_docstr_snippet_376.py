class WIC_1ENET(object):
    '''
    WIC-1ENET Ethernet
    '''

    def __init__(self):
        self._interfaces = 1

    def __str__(self):
        return "WIC-1ENET Ethernet"

    @property
    def interfaces(self):
        '''
        Returns the number of interfaces supported by this WIC.

        :returns: number of interfaces
        '''
        return self._interfaces