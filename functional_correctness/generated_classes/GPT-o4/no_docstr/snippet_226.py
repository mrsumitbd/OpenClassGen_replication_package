class Blink:
    def __init__(self, interval=1.0, callback=None):
        self.interval = interval
        self.callback = callback or self._default_callback
        self._stop_event = threading.Event()
        self._thread = None

    def _default_callback(self, state):
        print(f"{'ON' if state else 'OFF'}")

    def _run(self):
        state = False
        while not self._stop_event.is_set():
            state = not state
            self.callback(state)
            time.sleep(self.interval)

    def on(self):
        if self._thread is None or not self._thread.is_alive():
            self._stop_event.clear()
            self._thread = threading.Thread(target=self._run)
            self._thread.daemon = True
            self._thread.start()

    def off(self):
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            self._thread.join()