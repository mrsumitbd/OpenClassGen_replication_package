class ExtensionKey(object):

    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, o):
        if not isinstance(o, ExtensionKey):
            return False
        return self.name == o.name

    def __ne__(self, o):
        return not self.__eq__(o)