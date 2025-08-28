class ResponsePromise(object):
    def __init__(self, receiver, tag):
        self.receiver = receiver
        self.tag = tag
        self._result = None
        self._ready = False

    def get(self):
        if not self._ready:
            self._result = self.receiver.get_response(self.tag)
            self._ready = True
        return self._result

    def __iter__(self):
        return iter(self.get())