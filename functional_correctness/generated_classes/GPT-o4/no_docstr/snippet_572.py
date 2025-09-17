class DbConnection:
    def __init__(self):
        self._conn = None
        self._db_path = os.getenv("DB_PATH", ":memory:")

    def connection(self):
        if self._conn is None:
            self._conn = sqlite3.connect(self._db_path)
            self._conn.row_factory = sqlite3.Row
        return self._conn