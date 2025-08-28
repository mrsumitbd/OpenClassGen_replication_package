class Pool(object):
    '''A Pool of database connections.'''

    def __init__(self, connect_func, max_size=10):
        '''Creates a ConnectionPool.'''
        self._connect = connect_func
        self._max_size = max_size
        self._lock = threading.Condition()
        self._idle = []
        self._total = 0
        self._closed = False

    def get(self, blocking=True):
        '''Gets a connection.'''
        with self._lock:
            if self._closed:
                raise PoolAlreadyClosedError("Pool is closed")
            while True:
                if self._idle:
                    conn = self._idle.pop()
                    return _ConnectionProxy(conn, self)
                if self._total < self._max_size:
                    conn = self._connect()
                    self._total += 1
                    return _ConnectionProxy(conn, self)
                if not blocking:
                    return None
                self._lock.wait()
                if self._closed:
                    raise PoolAlreadyClosedError("Pool is closed")

    def _return(self, conn):
        with self._lock:
            if self._closed:
                try:
                    conn.close()
                except Exception:
                    pass
                self._total -= 1
            else:
                self._idle.append(conn)
            self._lock.notify()

    def close(self):
        '''Closes the pool and all idle connections.'''
        with self._lock:
            if self._closed:
                return
            self._closed = True
            for conn in self._idle:
                try:
                    conn.close()
                except Exception:
                    pass
                self._total -= 1
            self._idle = []
            self._lock.notify_all()