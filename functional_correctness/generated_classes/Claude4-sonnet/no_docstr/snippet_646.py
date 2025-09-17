class IDGenerator:
    def __init__(self):
        self._id_counter = 0
        self._function_ids = {}

    def ensure_id(self, fn_t):
        if fn_t not in self._function_ids:
            self._function_ids[fn_t] = self._id_counter
            self._id_counter += 1
        return self._function_ids[fn_t]