class WIC_1ENET(object):
    '''
    WIC-1ENET Ethernet
    '''

    def __init__(self):
        self.name = "WIC-1ENET"
        self.description = "WIC-1ENET Ethernet"

    def __str__(self):
        return self.name

    @property
    def interfaces(self):
        '''
        Returns the number of interfaces supported by this WIC.

        :returns: number of interfaces
        '''
        return 1