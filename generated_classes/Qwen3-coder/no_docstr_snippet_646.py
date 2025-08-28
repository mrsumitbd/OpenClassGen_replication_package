class IDGenerator:
    def __init__(self):
        self._id_counter = 0
        self._id_map = {}

    def ensure_id(self, fn_t):
        if fn_t not in self._id_map:
            self._id_map[fn_t] = self._id_counter
            self._id_counter += 1
        return self._id_map[fn_t]