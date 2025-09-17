class _TimeoutGarbageCollector:
    '''Base class for objects that periodically clean up timed-out waiters.

    Avoids memory leak in a common pattern like:

        while True:
            yield condition.wait(short_timeout)
            print('looping....')
    '''

    def __init__(self) -> None:
        self._waiters: Set[Any] = set()
        self._lock = threading.Lock()
        self._last_gc_time = time.time()
        self._gc_interval = 1.0

    def _garbage_collect(self) -> None:
        now = time.time()
        if now - self._last_gc_time < self._gc_interval:
            return
        
        with self._lock:
            expired_waiters = set()
            for waiter in self._waiters:
                if hasattr(waiter, '_timeout') and hasattr(waiter, '_start_time'):
                    if waiter._timeout is not None:
                        if now - waiter._start_time > waiter._timeout:
                            expired_waiters.add(waiter)
                elif hasattr(waiter, 'cancelled') and callable(waiter.cancelled):
                    if waiter.cancelled():
                        expired_waiters.add(waiter)
            
            self._waiters -= expired_waiters
            self._last_gc_time = now