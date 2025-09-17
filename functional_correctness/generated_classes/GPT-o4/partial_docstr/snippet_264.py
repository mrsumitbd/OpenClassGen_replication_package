class _TimeoutGarbageCollector:
    _instances = weakref.WeakSet()
    _lock = threading.Lock()
    _timer = None
    _interval = 60.0

    def __init__(self) -> None:
        cls = self.__class__
        with cls._lock:
            cls._instances.add(self)
            if cls._timer is None:
                cls._start()

    @classmethod
    def _start(cls):
        cls._timer = threading.Timer(cls._interval, cls._collect)
        cls._timer.daemon = True
        cls._timer.start()

    @classmethod
    def _collect(cls):
        for inst in list(cls._instances):
            try:
                inst._garbage_collect()
            except Exception:
                pass
        with cls._lock:
            if cls._instances:
                cls._start()
            else:
                cls._timer = None

    def _garbage_collect(self) -> None:
        pass