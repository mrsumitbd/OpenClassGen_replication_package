class MessageBuffer(object):

    def __init__(self):
        self._lock = threading.Lock()
        self._buffer = []  # list of (seq, message)
        self._next_seq = 1
        self._pending = []  # list of (future, cursor)

    def wait_for_messages(self, cursor=None):
        if cursor is None:
            cursor = 0
        fut = concurrent.futures.Future()
        with self._lock:
            new = [msg for seq, msg in self._buffer if seq > cursor]
            if new:
                fut.set_result(new)
            else:
                self._pending.append((fut, cursor))
        return fut

    def cancel_wait(self, future):
        with self._lock:
            for i, (fut, cursor) in enumerate(self._pending):
                if fut is future:
                    fut.cancel()
                    del self._pending[i]
                    break

    def new_messages(self, messages):
        with self._lock:
            for msg in messages:
                self._buffer.append((self._next_seq, msg))
                self._next_seq += 1
            to_notify = []
            for fut, cursor in self._pending:
                if fut.cancelled():
                    continue
                new = [msg for seq, msg in self._buffer if seq > cursor]
                if new:
                    to_notify.append((fut, new))
            for fut, new in to_notify:
                if not fut.done():
                    fut.set_result(new)
                self._pending = [(f, c) for f, c in self._pending if f is not fut]