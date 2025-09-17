class NonBlockingStreamReaderWriter:
    '''A non-blocking stream reader/writer
    '''

    def __init__(self, stream, print_stream=True, log_file=None):
        '''Initialize the stream reader/writer

        Positional arguments:
        stream -- the stream to read from.
                  Usually a process' stdout or stderr.
        log_file -- the file to write the stream output to
        '''
        self.stream = stream
        self.print_stream = print_stream
        self.queue = queue.Queue()
        if log_file:
            if isinstance(log_file, str):
                self.log_file_handle = open(log_file, 'a')
            else:
                self.log_file_handle = log_file
        else:
            self.log_file_handle = None
        self._thread = threading.Thread(
            target=self._populate_queue,
            args=(self.stream, self.queue, self.log_file_handle),
            daemon=True
        )
        self._thread.start()

    def _populate_queue(self, stream, queue, log_file_handle):
        ''' Collect lines from 'stream', put them in 'queue'.
            Write the stream output to the log_file if it was supplied.
        '''
        while True:
            line = stream.readline()
            if line == '' or line is None:
                break
            queue.put(line)
            if self.print_stream:
                sys.stdout.write(line)
                sys.stdout.flush()
            if log_file_handle:
                try:
                    log_file_handle.write(line)
                    log_file_handle.flush()
                except:
                    pass
        if log_file_handle and hasattr(log_file_handle, 'close'):
            try:
                log_file_handle.close()
            except:
                pass

    def get_all_output(self):
        lines = []
        try:
            while True:
                lines.append(self.queue.get_nowait())
        except queue.Empty:
            pass
        return lines

    def readline(self, timeout=0.1):
        '''Try to read a line from the stream queue.
        '''
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None