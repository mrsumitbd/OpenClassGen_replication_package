class _TimeoutGarbageCollector:
    '''Base class for objects that periodically clean up timed-out waiters.

    Avoids memory leak in a common pattern like:

        while True:
            yield condition.wait(short_timeout)
            print('looping....')
    '''

    def __init__(self) -> None:
        self._waiters = []
        self._garbage_collection_count = 0

    def _garbage_collect(self) -> None:
        # Clean up any waiters that have timed out
        self._waiters = [waiter for waiter in self._waiters if not waiter.done()]
        self._garbage_collection_count += 1