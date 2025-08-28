class ResponsePromise(object):
    def __init__(self, receiver, tag):
        self._receiver = receiver
        self._tag = tag

    def get(self):
        return self._receiver.get(self._tag)

    def __iter__(self):
        yield self.get()