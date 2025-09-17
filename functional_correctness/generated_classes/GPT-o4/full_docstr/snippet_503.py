class IFastPathSender(object):
    '''
    @summary: Fast path send capability
    '''

    def __init__(self):
        self._fastPathListener = None
        self._initialized = False

    def initFastPath(self, fastPathListener):
        '''
        @summary: initialize stack
        @param fastPathListener: {IFastPathListener}
        '''
        self.setFastPathListener(fastPathListener)
        self._initialized = True

    def setFastPathListener(self, fastPathListener):
        '''
        @param fastPathListener: {IFastPathListener}
        '''
        if not hasattr(fastPathListener, 'onFastPathData'):
            raise ValueError("Listener must implement onFastPathData(secFlag, data_bytes)")
        self._fastPathListener = fastPathListener

    def sendFastPath(self, secFlag, fastPathS):
        '''
        @summary: Send fastPathS Type as fast path packet
        @param secFlag: {integer} Security flag for fastpath packet
        @param fastPathS: {Type | Tuple} type transform to stream and send as fastpath
        '''
        if not self._initialized or self._fastPathListener is None:
            raise RuntimeError("FastPathSender not initialized with a listener")

        # convert fastPathS to bytes
        if isinstance(fastPathS, bytes):
            payload = fastPathS
        elif isinstance(fastPathS, str):
            payload = fastPathS.encode('utf-8')
        elif isinstance(fastPathS, tuple):
            parts = []
            for item in fastPathS:
                if isinstance(item, bytes):
                    parts.append(item)
                elif isinstance(item, str):
                    parts.append(item.encode('utf-8'))
                else:
                    parts.append(str(item).encode('utf-8'))
            payload = b''.join(parts)
        else:
            payload = str(fastPathS).encode('utf-8')

        # build header: 1 byte secFlag, 2 bytes payload length
        header = struct.pack('!BH', secFlag & 0xFF, len(payload))
        packet = header + payload

        # send packet to listener
        self._fastPathListener.onFastPathData(secFlag, packet)