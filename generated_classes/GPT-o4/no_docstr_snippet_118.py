class LineReader:
    def __init__(self, file_name):
        self._file_name = file_name
        self._file = open(file_name, 'r', encoding='utf-8')
        self._total_size = os.path.getsize(file_name)
        first = self._file.readline()
        self._next_line = first if first != '' else None

    def has_next(self):
        return self._next_line is not None

    def __next__(self):
        if self._next_line is None:
            self._file.close()
            raise StopIteration
        current = self._next_line
        nxt = self._file.readline()
        self._next_line = nxt if nxt != '' else None
        return current

    def __iter__(self):
        return self

    def get_progress(self):
        if self._total_size == 0:
            return 1.0
        return self._file.tell() / self._total_size