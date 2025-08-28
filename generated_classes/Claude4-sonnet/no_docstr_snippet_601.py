class Clock:
    def __init__(self, is_flat_out=False):
        self.is_flat_out = is_flat_out
        self.current_time = time.time()
        self.start_time = self.current_time

    def time(self):
        if self.is_flat_out:
            return self.current_time
        else:
            return time.time()

    def sleep(self, delta_time):
        if self.is_flat_out:
            self.current_time += delta_time
        else:
            time.sleep(delta_time)