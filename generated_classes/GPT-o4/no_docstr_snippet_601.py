class Clock:
    def __init__(self, is_flat_out=False):
        self.is_flat_out = is_flat_out
        if self.is_flat_out:
            self._t = 0.0
        else:
            self._start = time.time()

    def time(self):
        if self.is_flat_out:
            return self._t
        return time.time() - self._start

    def sleep(self, delta_time):
        if self.is_flat_out:
            self._t += delta_time
        else:
            time.sleep(delta_time)