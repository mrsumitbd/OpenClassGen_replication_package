class ServiceCheckStatus(object):

    def __init__(self, default_map, user_map):
        if default_map is None:
            default_map = {}
        if user_map is None:
            user_map = {}
        self._combined = dict(default_map)
        self._combined.update(user_map)

    def get(self, key):
        return self._combined.get(key)