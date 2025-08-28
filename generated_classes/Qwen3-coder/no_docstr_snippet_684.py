class MessageBuffer(object):
    def __init__(self):
        self._messages = deque()
        self._waiters = []
        self._lock = threading.RLock()
        self._cancelled = set()

    def wait_for_messages(self, cursor=None):
        future = asyncio.Future()
        
        with self._lock:
            # Check if there are already messages available
            if cursor is None:
                if len(self._messages) > 0:
                    future.set_result(list(self._messages))
                    return future
            else:
                # Find messages after cursor
                available_messages = []
                for msg in self._messages:
                    if hasattr(msg, 'id') and msg.id > cursor:
                        available_messages.append(msg)
                
                if available_messages:
                    future.set_result(available_messages)
                    return future
            
            # No messages available, add to waiters
            waiter_id = id(future)
            self._waiters.append((waiter_id, future, cursor))
            future._waiter_id = waiter_id
            
        return future

    def cancel_wait(self, future):
        if hasattr(future, '_waiter_id'):
            waiter_id = future._waiter_id
            with self._lock:
                self._cancelled.add(waiter_id)
                # Remove from waiters list
                self._waiters = [(wid, f, cursor) for wid, f, cursor in self._waiters if wid != waiter_id]
            
            if not future.done():
                future.cancel()

    def new_messages(self, messages):
        if not messages:
            return
            
        with self._lock:
            # Add new messages
            for msg in messages:
                self._messages.append(msg)
            
            # Notify waiting futures
            notified_waiters = []
            for waiter_id, future, cursor in self._waiters:
                if waiter_id in self._cancelled:
                    continue
                    
                try:
                    if cursor is None:
                        # Return all messages
                        future.set_result(list(self._messages))
                        notified_waiters.append(waiter_id)
                    else:
                        # Return messages after cursor
                        available_messages = []
                        for msg in self._messages:
                            if hasattr(msg, 'id') and msg.id > cursor:
                                available_messages.append(msg)
                        
                        if available_messages:
                            future.set_result(available_messages)
                            notified_waiters.append(waiter_id)
                except Exception as e:
                    future.set_exception(e)
                    notified_waiters.append(waiter_id)
            
            # Remove notified waiters
            self._waiters = [(wid, f, cursor) for wid, f, cursor in self._waiters 
                           if wid not in notified_waiters and wid not in self._cancelled]
            
            # Clean up cancelled set
            for waiter_id in list(self._cancelled):
                if waiter_id not in [wid for wid, _, _ in self._waiters]:
                    self._cancelled.discard(waiter_id)