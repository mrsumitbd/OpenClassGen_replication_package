class User(object):

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"User({self.id}, '{self.name}')"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id and self.name == other.name