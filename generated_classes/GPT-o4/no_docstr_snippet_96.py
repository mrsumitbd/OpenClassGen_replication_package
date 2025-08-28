class Timer(object):
    def __init__(self, func):
        self.func = func
        self._running = False
        self._thread = None

    def on_timer(self):
        self.func()

    def start(self):
        if self._running:
            return
        self._running = True
        def _run():
            while self._running:
                time.sleep(1)
                self.on_timer()
        self._thread = threading.Thread(target=_run)
        self._thread.daemon = True
        self._thread.start()