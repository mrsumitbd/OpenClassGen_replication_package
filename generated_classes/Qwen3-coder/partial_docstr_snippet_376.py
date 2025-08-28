class WIC_1ENET(object):
    '''
    WIC-1ENET Ethernet
    '''

    def __init__(self):
        pass

    def __str__(self):
        return "WIC-1ENET"

    @property
    def interfaces(self):
        '''
        Returns the number of interfaces supported by this WIC.

        :returns: number of interfaces
        '''
        return 1