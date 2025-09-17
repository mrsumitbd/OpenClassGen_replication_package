class IDGenerator:
    def __init__(self):
        self._ids = {}
        self._next_id = 0

    def ensure_id(self, fn_t):
        if fn_t not in self._ids:
            self._ids[fn_t] = self._next_id
            self._next_id += 1
        return self._ids[fn_t]