class NodeCommands:
    '''Node-level command pipeline for Redis-like connections'''

    def __init__(self, parse_response, connection_pool, connection=None):
        self.parse_response = parse_response
        self.connection_pool = connection_pool
        self.connection = connection
        self._commands = []
        self._pending_count = 0

    def append(self, c):
        self._commands.append(c)

    def write(self):
        if not self.connection:
            self.connection = self.connection_pool.get_connection()
        try:
            self._pending_count = len(self._commands)
            for cmd in self._commands:
                # each cmd is expected to be bytes or bytearray
                self.connection.sendall(cmd)
        except Exception:
            try:
                self.connection.disconnect()
            except Exception:
                pass
            self.connection = None
            raise
        finally:
            self._commands = []

    def read(self):
        if not self.connection:
            raise RuntimeError("No connection available for reading")
        results = []
        try:
            for _ in range(self._pending_count):
                results.append(self.parse_response(self.connection))
            return results
        finally:
            self._pending_count = 0
            try:
                self.connection_pool.release(self.connection)
            except Exception:
                pass
            self.connection = None