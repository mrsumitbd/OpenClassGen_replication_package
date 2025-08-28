class Client(object):
    def __init__(self, url, principal=None):
        self.url = url
        self.principal = principal
        self.entities = {}

    def list_all_entities(self, ent_name):
        if ent_name in self.entities:
            return self.entities[ent_name]
        else:
            return []