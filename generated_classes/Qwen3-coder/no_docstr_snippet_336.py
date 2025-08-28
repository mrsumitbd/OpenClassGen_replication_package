class ResponsePromise(object):
    def __init__(self, receiver, tag):
        self._receiver = receiver
        self._tag = tag
        self._result = None
        self._resolved = False

    def get(self):
        if not self._resolved:
            self._result = self._receiver.receive(self._tag)
            self._resolved = True
        return self._result

    def __iter__(self):
        yield self.get()