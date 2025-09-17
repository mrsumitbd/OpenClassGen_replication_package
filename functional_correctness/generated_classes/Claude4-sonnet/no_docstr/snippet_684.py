class MessageBuffer(object):
    def __init__(self):
        self._messages = deque()
        self._waiters = []
        self._lock = threading.Lock()
        self._message_id = 0

    def wait_for_messages(self, cursor=None):
        with self._lock:
            if cursor is None:
                cursor = 0
            
            # Check if we have messages after the cursor
            available_messages = []
            for msg_id, message in self._messages:
                if msg_id > cursor:
                    available_messages.append((msg_id, message))
            
            if available_messages:
                # Return immediately if we have messages
                future = asyncio.Future()
                future.set_result(available_messages)
                return future
            
            # No messages available, create a future to wait
            future = asyncio.Future()
            self._waiters.append((cursor, future))
            return future

    def cancel_wait(self, future):
        with self._lock:
            self._waiters = [(cursor, f) for cursor, f in self._waiters if f != future]
            if not future.done():
                future.cancel()

    def new_messages(self, messages):
        with self._lock:
            # Add messages to buffer
            for message in messages:
                self._message_id += 1
                self._messages.append((self._message_id, message))
            
            # Notify waiters
            completed_waiters = []
            for cursor, future in self._waiters:
                if not future.done():
                    # Get messages after cursor
                    available_messages = []
                    for msg_id, message in self._messages:
                        if msg_id > cursor:
                            available_messages.append((msg_id, message))
                    
                    if available_messages:
                        future.set_result(available_messages)
                        completed_waiters.append((cursor, future))
            
            # Remove completed waiters
            for waiter in completed_waiters:
                if waiter in self._waiters:
                    self._waiters.remove(waiter)