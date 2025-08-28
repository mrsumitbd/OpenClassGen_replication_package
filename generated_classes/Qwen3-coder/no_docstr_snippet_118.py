class LineReader:
    def __init__(self, file_name):
        self.file_name = file_name
        self.file = open(file_name, 'r')
        self.current_line = None
        self._eof = False
        self._total_size = self._get_file_size()
        self._bytes_read = 0

    def _get_file_size(self):
        current_pos = self.file.tell()
        self.file.seek(0, 2)  # Seek to end
        size = self.file.tell()
        self.file.seek(current_pos)  # Return to original position
        return size

    def has_next(self):
        if self._eof:
            return False
        # Peek at the next line
        current_pos = self.file.tell()
        line = self.file.readline()
        self.file.seek(current_pos)
        if line == '':
            self._eof = True
            return False
        return True

    def __next__(self):
        if not self.has_next():
            raise StopIteration
        line = self.file.readline()
        if line == '':
            raise StopIteration
        self._bytes_read = self.file.tell()
        self.current_line = line.rstrip('\n')
        return self.current_line

    def __iter__(self):
        return self

    def get_progress(self):
        if self._total_size == 0:
            return 1.0
        return min(self._bytes_read / self._total_size, 1.0)

    def __del__(self):
        if hasattr(self, 'file') and not self.file.closed:
            self.file.close()