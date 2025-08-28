class PDUClientListener(object):
    '''
    @summary: Interface for PDU client automata listener
    '''

    def onReady(self):
        '''
        @summary: Event call when PDU layer is ready to send events
        '''
        pass

    def onSessionReady(self):
        '''
        @summary: Event call when Windows session is ready
        '''
        pass

    def onUpdate(self, rectangles):
        '''
        @summary: call when a bitmap data is received from update PDU
        @param rectangles: [pdu.BitmapData] struct
        '''
        pass

    def recvDstBltOrder(self, order):
        '''
        @param order: rectangle order
        '''
        pass