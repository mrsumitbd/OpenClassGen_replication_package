class ExecutionListener(object):
    def __init__(self, cfg):
        self.cfg = cfg or {}
        self.log_to_console = self.cfg.get('console', True)
        self.log_file_path = self.cfg.get('log_file')
        self._lock = threading.Lock()
        self._file = None
        if self.log_file_path:
            self._file = open(self.log_file_path, 'a', encoding='utf-8')

    def context_changed(self, context):
        timestamp = datetime.datetime.utcnow().isoformat()
        msg = f"{timestamp} - CONTEXT_CHANGED - {context}\n"
        self._emit(msg)

    def response_returned(self, context, response):
        timestamp = datetime.datetime.utcnow().isoformat()
        msg = f"{timestamp} - RESPONSE_RETURNED - context={context} response={response}\n"
        self._emit(msg)

    def _emit(self, message):
        with self._lock:
            if self.log_to_console:
                print(message, end='')
            if self._file:
                self._file.write(message)
                self._file.flush()

    def __del__(self):
        if self._file:
            try:
                self._file.close()
            except Exception:
                pass