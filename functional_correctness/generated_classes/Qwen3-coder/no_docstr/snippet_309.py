class Backend:
    def __init__(self, options):
        self.options = options
        self.connection = None

    def do_createdb(self):
        # Implementation for creating database
        raise NotImplementedError("Subclasses must implement do_createdb")

    def do_dropdb(self):
        # Implementation for dropping database
        raise NotImplementedError("Subclasses must implement do_dropdb")

    def connect(self):
        # Implementation for connecting to database
        raise NotImplementedError("Subclasses must implement connect")

    def close(self):
        # Implementation for closing database connection
        if self.connection:
            self.connection.close()
            self.connection = None

    def createdb(self):
        # Wrapper method for creating database
        try:
            self.do_createdb()
        except Exception as e:
            raise Exception(f"Failed to create database: {str(e)}")

    def dropdb(self):
        # Wrapper method for dropping database
        try:
            self.do_dropdb()
        except Exception as e:
            raise Exception(f"Failed to drop database: {str(e)}")