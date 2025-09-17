class IFastPathSender(object):
    '''
    @summary: Fast path send capability
    '''

    def sendFastPath(self, secFlag, fastPathS):
        '''
        @summary: Send fastPathS Type as fast path packet
        @param secFlag: {integer} Security flag for fastpath packet
        @param fastPathS: {Type | Tuple} type transform to stream and send as fastpath
        '''
        pass

    def initFastPath(self, fastPathListener):
        '''
        @summary: initialize stack
        @param fastPathListener: {IFastPathListener}
        '''
        pass

    def setFastPathListener(self, fastPathListener):
        '''
        @param fastPathListener: {IFastPathListener}
        '''
        pass