class LLDPConfiguration(object):
    '''
    basic configuration for LLDP layer
    '''

    def __init__(self):
        self._strict_mode = False

    def strict_mode_enable(self):
        '''
        enable strict mode and dissector debugging
        '''
        self._strict_mode = True

    def strict_mode_disable(self):
        '''
        disable strict mode and dissector debugging
        '''
        self._strict_mode = False

    def strict_mode_get(self):
        '''
        get current strict mode state
        '''
        return self._strict_mode