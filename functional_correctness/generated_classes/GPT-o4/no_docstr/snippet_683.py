class User(object):
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r})"

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented
        return self.id == other.id and self.name == other.name