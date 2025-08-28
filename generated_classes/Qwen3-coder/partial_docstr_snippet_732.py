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
        self._connections = queue.Queue(maxsize=max_size)
        self._created_connections = 0
        self._lock = threading.Lock()
        self._closed = False

        # Pre-populate the pool with connections
        for _ in range(max_size):
            conn = self._connect_func()
            self._connections.put(conn)
            self._created_connections += 1

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
        with self._lock:
            if self._closed:
                raise PoolAlreadyClosedError("Pool is already closed")

        try:
            return self._connections.get(blocking=blocking)
        except queue.Empty:
            return None

    def put(self, connection):
        '''Returns a connection to the pool.

        Args:
          connection: A connection to return to the pool.
        '''
        with self._lock:
            if self._closed:
                connection.close()
                return

        try:
            self._connections.put(connection, block=False)
        except queue.Full:
            # If the pool is full, close the connection
            connection.close()

    def close(self):
        with self._lock:
            if self._closed:
                return
            self._closed = True

        # Close all connections in the pool
        while not self._connections.empty():
            try:
                conn = self._connections.get_nowait()
                conn.close()
            except queue.Empty:
                break