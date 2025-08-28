class DbConnection:
    def __init__(self):
        self.db_path = ":memory:"
        self._connection = None

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()