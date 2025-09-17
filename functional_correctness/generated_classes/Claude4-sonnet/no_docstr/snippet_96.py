class Timer(object):
    def __init__(self, func):
        self.func = func
        self.timer = None
        self.is_running = False

    def on_timer(self):
        self.is_running = False
        self.func()

    def start(self, interval=1.0):
        if not self.is_running:
            self.timer = threading.Timer(interval, self.on_timer)
            self.timer.start()
            self.is_running = True

    def stop(self):
        if self.timer:
            self.timer.cancel()
            self.is_running = False