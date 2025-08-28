class AsynchronousResponseIterator:
    def __init__(self, response_buffor_manager):
        self._mgr = response_buffor_manager
        self._finished = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._finished:
            raise StopIteration
        try:
            item = next(self._mgr)
        except StopIteration:
            self._finished = True
            raise
        return item

    @property
    def end_of_buffered(self):
        return self._finished