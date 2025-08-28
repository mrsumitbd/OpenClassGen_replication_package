class WIC_1T(object):
    '''
    WIC-1T Serial
    '''

    def __init__(self):
        self._name = "WIC-1T"
        self._description = "1-port serial WIC"
        self._interface_count = 1

    def __str__(self):
        return self._name

    @property
    def interfaces(self):
        '''
        Returns the number of interfaces supported by this WIC.

        :returns: number of interfaces
        '''
        return self._interface_count