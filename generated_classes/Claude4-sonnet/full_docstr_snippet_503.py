class IFastPathSender(object):
    '''
    @summary: Fast path send capability
    '''

    def __init__(self):
        self._fastPathListener = None

    def sendFastPath(self, secFlag, fastPathS):
        '''
        @summary: Send fastPathS Type as fast path packet
        @param secFlag: {integer} Security flag for fastpath packet
        @param fastPathS: {Type | Tuple} type transform to stream and send as fastpath
        '''
        raise NotImplementedError("sendFastPath method must be implemented")

    def initFastPath(self, fastPathListener):
        '''
        @summary: initialize stack
        @param fastPathListener: {IFastPathListener}
        '''
        self._fastPathListener = fastPathListener

    def setFastPathListener(self, fastPathListener):
        '''
        @param fastPathListener: {IFastPathListener}
        '''
        self._fastPathListener = fastPathListener