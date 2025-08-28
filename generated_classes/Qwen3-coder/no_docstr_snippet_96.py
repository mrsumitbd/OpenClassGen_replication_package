class Timer(object):
    def __init__(self, func):
        self.func = func
        self.timer = None
        self.running = False

    def on_timer(self):
        if self.running:
            self.func()
            self.start()

    def start(self):
        if not self.running:
            self.running = True
            self.timer = threading.Timer(1.0, self.on_timer)
            self.timer.start()

    def stop(self):
        self.running = False
        if self.timer:
            self.timer.cancel()