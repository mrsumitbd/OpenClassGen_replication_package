class GrpcManager:
    '''
    Class for managing GRPC calls by turing the generators grpc uses into function calls
    This allows the sdk to man in the middle the messages
    '''

    def __init__(self, stub_call, on_msg_callback, metadata, tx_stream=True, initial_message=None):
        '''
        :param stub_call: the call on the grpc stub to build the generator on
        :param on_msg_callback: the callback to pass any received functions on
        :param metadata: metadata to attach to the stub call
        '''
        self.stub_call = stub_call
        self.on_msg_callback = on_msg_callback
        self.metadata = metadata
        self.tx_stream = tx_stream
        self.initial_message = initial_message
        
        self.grpc_tx_queue = queue.Queue()
        self.generator = None
        self.rx_thread = None
        self.stop_event = threading.Event()
        
        # Start the grpc communication
        self._start_grpc_communication()

    def send_message(self, tx_message):
        '''
        Add a message onto the tx queue to be sent on the stub
        :param tx_message:
        :return: None
        '''
        self.grpc_tx_queue.put(tx_message)

    def _grpc_rx_receiver(self):
        '''
        Blocking Function that opens the stubs generator and pass any messages onto the callback
        :return: None
        '''
        try:
            for message in self.generator:
                if self.stop_event.is_set():
                    break
                if self.on_msg_callback:
                    self.on_msg_callback(message)
        except Exception:
            pass  # Handle generator closing or errors

    def stop_generator(self):
        '''
        Call this to close the generator
        :return:
        '''
        self.stop_event.set()
        if self.rx_thread and self.rx_thread.is_alive():
            self.rx_thread.join()

    def _grpc_tx_generator(self):
        '''
        the generator taking and messages added to the grpc_tx_queue
        and yield them to grpc
        :return: grpc messages
        '''
        if self.initial_message is not None:
            yield self.initial_message
            
        while not self.stop_event.is_set():
            try:
                message = self.grpc_tx_queue.get(timeout=0.1)
                yield message
            except queue.Empty:
                continue

    def _start_grpc_communication(self):
        '''
        Internal method to start the grpc communication threads
        '''
        if self.tx_stream:
            self.generator = self.stub_call(self._grpc_tx_generator(), metadata=self.metadata)
        else:
            self.generator = self.stub_call(metadata=self.metadata)
            
        self.rx_thread = threading.Thread(target=self._grpc_rx_receiver)
        self.rx_thread.daemon = True
        self.rx_thread.start()