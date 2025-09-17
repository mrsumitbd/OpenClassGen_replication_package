class GrpcManager:
    '''
    Class for managing GRPC calls by turning the generators grpc uses into function calls.
    This allows the sdk to man in the middle the messages.
    '''

    def __init__(self, stub_call, on_msg_callback, metadata, tx_stream=True, initial_message=None):
        '''
        :param stub_call: the call on the grpc stub to build the generator on
        :param on_msg_callback: the callback to pass any received messages on
        :param metadata: metadata to attach to the stub call
        :param tx_stream: whether this is a streaming (bi-di) call
        :param initial_message: optional first message to send on tx_stream
        '''
        self.stub_call = stub_call
        self.on_msg_callback = on_msg_callback
        self.metadata = metadata
        self.tx_stream = tx_stream
        self.initial_message = initial_message

        self._stop_event = threading.Event()
        self._grpc_tx_queue = queue.Queue()
        self._sentinel = object()
        self._thread = None

        if self.tx_stream:
            # start the streaming call
            self._call = self.stub_call(
                self._grpc_tx_generator(),
                metadata=self.metadata
            )
            self._thread = threading.Thread(target=self._grpc_rx_receiver, daemon=True)
            self._thread.start()
        else:
            # unary or server-streaming with a single request
            resp = self.stub_call(self.initial_message, metadata=self.metadata)
            # if it's a generator, iterate; else treat as single response
            if hasattr(resp, '__iter__') and not isinstance(resp, (bytes, str)):
                for msg in resp:
                    self.on_msg_callback(msg)
            else:
                self.on_msg_callback(resp)

    def send_message(self, tx_message):
        '''
        Add a message onto the tx queue to be sent on the stub
        :param tx_message:
        :return: None
        '''
        if not self.tx_stream:
            raise RuntimeError("send_message called on non-streaming GrpcManager")
        if self._stop_event.is_set():
            raise RuntimeError("Cannot send message after stop_generator()")
        self._grpc_tx_queue.put(tx_message)

    def _grpc_rx_receiver(self):
        '''
        Blocking function that opens the stub's generator and passes any messages onto the callback
        :return: None
        '''
        try:
            for msg in self._call:
                if self._stop_event.is_set():
                    break
                self.on_msg_callback(msg)
        finally:
            # ensure we mark stop and unblock tx_generator
            self._stop_event.set()
            # put sentinel in case tx_generator is waiting
            self._grpc_tx_queue.put(self._sentinel)

    def stop_generator(self):
        '''
        Call this to close the generator
        :return: None
        '''
        if not self.tx_stream:
            return
        # signal stop
        self._stop_event.set()
        # unblock tx generator if waiting
        self._grpc_tx_queue.put(self._sentinel)
        # wait for rx thread to finish
        if self._thread is not None:
            self._thread.join()
            self._thread = None

    def _grpc_tx_generator(self):
        '''
        The generator taking any messages added to the grpc_tx_queue
        and yielding them to grpc
        :return: grpc messages
        '''
        # send initial message if provided
        if self.initial_message is not None:
            yield self.initial_message
            self.initial_message = None

        while not self._stop_event.is_set():
            msg = self._grpc_tx_queue.get()
            if msg is self._sentinel:
                break
            yield msg

        # clean up remaining items if any
        while not self._grpc_tx_queue.empty():
            try:
                m = self._grpc_tx_queue.get_nowait()
                if m is self._sentinel:
                    break
            except queue.Empty:
                break