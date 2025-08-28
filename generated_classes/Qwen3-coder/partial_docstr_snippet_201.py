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
        self.log_file = log_file
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._populate_queue, 
                                     args=(self.stream, self.queue, self.log_file))
        self.thread.daemon = True
        self.thread.start()

    def _populate_queue(self, stream, queue, log_file):
        ''' Collect lines from 'stream', put them in 'queue'.
        Write the stream output to the log_file if it was supplied.
        '''
        logfile_handle = None
        if log_file:
            logfile_handle = open(log_file, 'w')
        
        try:
            for line in iter(stream.readline, ''):
                queue.put(line)
                if self.print_stream:
                    sys.stdout.write(line)
                    sys.stdout.flush()
                if logfile_handle:
                    logfile_handle.write(line)
                    logfile_handle.flush()
        finally:
            if logfile_handle:
                logfile_handle.close()

    def get_all_output(self):
        lines = []
        while not self.queue.empty():
            try:
                lines.append(self.queue.get_nowait())
            except queue.Empty:
                break
        return lines

    def readline(self, timeout=0.1):
        '''Try to read a line from the stream queue.
        '''
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None