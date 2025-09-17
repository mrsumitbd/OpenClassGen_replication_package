class BumperClient:
    def __init__(self, ic, prefix, start=False):
        self._ic = ic
        self._topic = f"{prefix}/bumper"
        self._sub = None
        self._lock = threading.Lock()
        self._data = None
        if start:
            self.start()

    def start(self):
        if self._sub is None:
            # ic.subscribe should return a handle with an unsubscribe() method
            self._sub = self._ic.subscribe(self._topic, self._on_message)

    def stop(self):
        if self._sub is not None:
            try:
                self._sub.unsubscribe()
            except AttributeError:
                # fallback if unsubscribe is on the ic itself
                self._ic.unsubscribe(self._sub)
            finally:
                self._sub = None

    def _on_message(self, msg):
        with self._lock:
            self._data = msg

    def getBumperData(self):
        with self._lock:
            return self._data