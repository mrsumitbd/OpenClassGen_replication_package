class LineReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name, 'r')
        self.file.seek(0, 2)
        self.total_size = self.file.tell()
        self.file.seek(0)
        self.current_position = 0
        self._next_line = None
        self._has_next = True
        self._peek_next()

    def _peek_next(self):
        try:
            self._next_line = self.file.readline()
            if not self._next_line:
                self._has_next = False
                self.file.close()
            else:
                self.current_position = self.file.tell()
        except:
            self._has_next = False
            self.file.close()

    def has_next(self):
        return self._has_next

    def __next__(self):
        if not self._has_next:
            raise StopIteration
        
        line = self._next_line.rstrip('\n\r')
        self._peek_next()
        return line

    def __iter__(self):
        return self

    def get_progress(self):
        if self.total_size == 0:
            return 1.0
        return min(1.0, self.current_position / self.total_size)