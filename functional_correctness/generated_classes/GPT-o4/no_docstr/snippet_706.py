class Database:
    def __init__(self, name):
        self.name = name

    def create_statement(self):
        return f"CREATE DATABASE {self.name};"

    def drop_statement(self):
        return f"DROP DATABASE {self.name};"

    def __repr__(self):
        return f"Database({self.name!r})"