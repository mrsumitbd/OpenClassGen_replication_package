class Backend:
    def __init__(self, options):
        self.options = options
        self.connection = None
        self.db_exists = False

    def do_createdb(self):
        if not self.db_exists:
            self.db_exists = True
            return True
        return False

    def do_dropdb(self):
        if self.db_exists:
            self.db_exists = False
            return True
        return False

    def connect(self):
        if self.connection is None:
            self.connection = f"connection_to_{self.options.get('database', 'default_db')}"
        return self.connection

    def close(self):
        if self.connection is not None:
            self.connection = None
            return True
        return False

    def createdb(self):
        try:
            return self.do_createdb()
        except Exception:
            return False

    def dropdb(self):
        try:
            return self.do_dropdb()
        except Exception:
            return False