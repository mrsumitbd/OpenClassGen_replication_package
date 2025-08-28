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
        self.queue = queue.Queue()
        self.threads = []
        self._stop_event = threading.Event()
        
        for _ in range(self.size):
            thread = threading.Thread(target=self._consume_queue)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def _consume_queue(self):
        '''
        Continually blocks until data is on the internal queue, then calls
        the session's registered callback and sends a PublishMessageReceived
        if callback returned True.
        '''
        while not self._stop_event.is_set():
            try:
                item = self.queue.get(timeout=1)
                if item is None:
                    break
                    
                session, block_id, data = item
                
                # Call the session's callback
                callback_result = session.callback(block_id, data)
                
                # If callback returned True and we have a write_queue, send PublishMessageReceived
                if callback_result and self.write_queue is not None:
                    # Assuming PublishMessageReceived is some message type to be sent
                    # This would depend on the specific implementation details
                    publish_message = {
                        'type': 'PublishMessageReceived',
                        'block_id': block_id,
                        'session_id': getattr(session, 'id', None)
                    }
                    self.write_queue.put(publish_message)
                    
                self.queue.task_done()
            except queue.Empty:
                continue
            except Exception:
                # Handle any exceptions that might occur during callback execution
                if not self.queue.empty():
                    self.queue.task_done()
                continue

    def queue_callback(self, session, block_id, data):
        '''
        Queues up a callback event to occur for a session with the given
        payload data.  Will block if the queue is full.

        :param session: the session with a defined callback function to call.
        :param block_id: the block_id of the message received.
        :param data: the data payload of the message received.
        '''
        self.queue.put((session, block_id, data))