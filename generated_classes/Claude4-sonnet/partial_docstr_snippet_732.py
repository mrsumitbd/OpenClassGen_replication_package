class Pool(object):
    '''A Pool of database connections.

  A simple pool, with a maximum number of simultaneous connections. Primary goal
  is to do the right thing when using MySQLdb in obvious ways (our use case),
  but we also try to stay loosely within the PEP-249 standard.

  Intends to be thread safe in that multiple connections can be requested and
  used by multiple threads without synchronization, but operations on each
  connection (and its associated cursors) are assumed to be serial.
  '''

    def __init__(self, connect_func, max_size=10):
        '''Creates a ConnectionPool.

        Args:
         connect_func: A closure which returns a new connection to the underlying
           database, i.e. a MySQLdb.Connection. Should raise or block if the
           database is unavailable.
         max_size: The maximum number of simultaneous connections.
        '''
        self._connect_func = connect_func
        self._max_size = max_size
        self._pool = queue.Queue(maxsize=max_size)
        self._lock = threading.Lock()
        self._closed = False
        self._created_connections = 0

    def get(self, blocking=True):
        '''Gets a connection.

        Args:
          blocking: Whether to block when max_size connections are already in use.
            If false, may return None.

        Returns:
          A connection to the database.

        Raises:
          PoolAlreadyClosedError: if close() method was already called on
          this pool.
        '''
        if self._closed:
            raise PoolAlreadyClosedError("Pool has been closed")

        try:
            connection = self._pool.get(block=False)
            return PooledConnection(connection, self)
        except queue.Empty:
            with self._lock:
                if self._closed:
                    raise PoolAlreadyClosedError("Pool has been closed")
                
                if self._created_connections < self._max_size:
                    connection = self._connect_func()
                    self._created_connections += 1
                    return PooledConnection(connection, self)
            
            if blocking:
                if self._closed:
                    raise PoolAlreadyClosedError("Pool has been closed")
                connection = self._pool.get(block=True)
                return PooledConnection(connection, self)
            else:
                return None

    def _return_connection(self, connection):
        if not self._closed:
            try:
                self._pool.put(connection, block=False)
            except queue.Full:
                pass

    def close(self):
        with self._lock:
            self._closed = True
            while not self._pool.empty():
                try:
                    connection = self._pool.get(block=False)
                    if hasattr(connection, 'close'):
                        connection.close()
                except queue.Empty:
                    break