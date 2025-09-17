class PDUClientListener(ABC):
    """
    @summary: Interface for PDU client automata listener
    """

    @abstractmethod
    def onReady(self):
        """
        @summary: Event call when PDU layer is ready to send events
        """
        raise NotImplementedError()

    @abstractmethod
    def onSessionReady(self):
        """
        @summary: Event call when Windows session is ready
        """
        raise NotImplementedError()

    @abstractmethod
    def onUpdate(self, rectangles):
        """
        @summary: call when a bitmap data is received from update PDU
        @param rectangles: [pdu.BitmapData] struct
        """
        raise NotImplementedError()

    @abstractmethod
    def recvDstBltOrder(self, order):
        """
        @param order: rectangle order
        """
        raise NotImplementedError()