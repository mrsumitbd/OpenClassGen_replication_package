class Backend:

    def __init__(self, options):
        self.options = options
        self.conn = None

    def do_createdb(self):
        self.connect()

    def do_dropdb(self):
        db = self.options.get('database', ':memory:')
        if db != ':memory:' and os.path.exists(db):
            os.remove(db)

    def connect(self):
        if self.conn is None:
            db = self.options.get('database', ':memory:')
            self.conn = sqlite3.connect(db)
        return self.conn

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None

    def createdb(self):
        self.do_createdb()
        self.close()

    def dropdb(self):
        self.close()
        self.do_dropdb()