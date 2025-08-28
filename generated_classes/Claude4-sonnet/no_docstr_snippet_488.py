class ServiceCheckStatus(object):

    def __init__(self, default_map, user_map):
        self.default_map = default_map
        self.user_map = user_map

    def get(self, key):
        if key in self.user_map:
            return self.user_map[key]
        elif key in self.default_map:
            return self.default_map[key]
        else:
            return None