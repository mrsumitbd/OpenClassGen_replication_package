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
        self.thread = threading.Thread(target=self._populate_queue, args=(stream, self.queue, log_file))
        self.thread.daemon = True
        self.thread.start()

    def _populate_queue(self, stream, queue, log_file):
        ''' Collect lines from 'stream', put them in 'queue'.
            Write the stream output to the log_file if it was supplied.
            '''
        try:
            for line in iter(stream.readline, b''):
                if isinstance(line, bytes):
                    line = line.decode('utf-8', errors='replace')
                line = line.rstrip('\n\r')
                if line:
                    queue.put(line)
                    if self.print_stream:
                        print(line)
                    if log_file:
                        with open(log_file, 'a') as f:
                            f.write(line + '\n')
        except:
            pass
        finally:
            stream.close()

    def get_all_output(self):
        lines = []
        while True:
            try:
                line = self.queue.get_nowait()
                lines.append(line)
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