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
        self._write_queue = write_queue
        self._queue = queue.Queue()
        self._threads = []
        for _ in range(size):
            t = threading.Thread(target=self._consume_queue)
            t.daemon = True
            t.start()
            self._threads.append(t)

    def _consume_queue(self):
        '''
        Continually blocks until data is on the internal queue, then calls
        the session's registered callback and sends a PublishMessageReceived
        if callback returned True.
        '''
        while True:
            session, block_id, data = self._queue.get()
            try:
                cb = getattr(session, 'callback', None)
                result = False
                if callable(cb):
                    result = cb(block_id, data)
                if result and self._write_queue:
                    # queue a write event for a PublishMessageReceived
                    self._write_queue.put((session, block_id))
            except Exception:
                pass
            finally:
                self._queue.task_done()

    def queue_callback(self, session, block_id, data):
        '''
        Queues up a callback event to occur for a session with the given
        payload data.  Will block if the queue is full.

        :param session: the session with a defined callback function to call.
        :param block_id: the block_id of the message received.
        :param data: the data payload of the message received.
        '''
        self._queue.put((session, block_id, data))