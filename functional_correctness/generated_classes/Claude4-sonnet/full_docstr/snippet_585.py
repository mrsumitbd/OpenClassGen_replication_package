class CallbackWorkerPool(object):
    '''
    A Worker Pool implementation that creates a number of predefined threads
    used for invoking Session callbacks.
    '''

    def __init__(self, write_queue=None, size=1):
        '''
        Creates a Callback Worker Pool for use in invoking Session Callbacks
        when data is received by a push client.

        :param write_queue: Queue used for queueing up socket write events
            for when a payload message is received and processed.
        :param size: The number of worker threads to invoke callbacks.
        '''
        self.write_queue = write_queue
        self.size = size
        self.callback_queue = queue.Queue()
        self.workers = []
        self.running = True
        
        for _ in range(size):
            worker = threading.Thread(target=self._consume_queue)
            worker.daemon = True
            worker.start()
            self.workers.append(worker)

    def _consume_queue(self):
        '''
        Continually blocks until data is on the internal queue, then calls
        the session's registered callback and sends a PublishMessageReceived
        if callback returned True.
        '''
        while self.running:
            try:
                session, block_id, data = self.callback_queue.get(timeout=1)
                if session.callback:
                    result = session.callback(block_id, data)
                    if result and self.write_queue:
                        self.write_queue.put(('PublishMessageReceived', session, block_id))
                self.callback_queue.task_done()
            except queue.Empty:
                continue
            except:
                break

    def queue_callback(self, session, block_id, data):
        '''
        Queues up a callback event to occur for a session with the given
        payload data.  Will block if the queue is full.

        :param session: the session with a defined callback function to call.
        :param block_id: the block_id of the message received.
        :param data: the data payload of the message received.
        '''
        self.callback_queue.put((session, block_id, data))