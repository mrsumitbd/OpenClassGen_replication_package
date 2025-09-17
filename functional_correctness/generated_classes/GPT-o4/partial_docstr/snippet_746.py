class CustomLogger:
    '''Helper Logger to redirect STDOUT or STDERR to a logging handler.

    It wraps a Logger class into a file like object, which provides a handy
    way to redirect STDOUT or STDERR to a logger. This class provides the
    necessary methods (write, flush and close) to build a file-like object
    and it can not be used directly as it does not provide a logging handler.
    Instead, you must instantiate one of subclass (CustomRotatingFileLogger and
    CustomUdpLogger).

    Arguments
        handler (logging.Handler): A logging handler to use.

    Methods:
        write(string): Write string to logger with newlines removed.
        flush(): Flush logger messages.
        close(): Close logger.

    Returns:
        A logger object.
    '''

    def __init__(self, handler):
        '''Create a logging.Logger class with extended functionality.'''
        self.handler = handler
        name = f"CustomLogger-{uuid.uuid4()}"
        self.logger = logging.getLogger(name)
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def write(self, string):
        '''Erase newline from a string and write to the logger.'''
        text = string.rstrip('\n')
        if text:
            for line in text.splitlines():
                self.logger.info(line)

    def flush(self):
        '''Flush logger's data.'''
        for h in self.logger.handlers:
            try:
                h.flush()
            except Exception:
                pass

    def close(self):
        '''Call the closer method of the logger.'''
        for h in list(self.logger.handlers):
            try:
                h.close()
            except Exception:
                pass
            self.logger.removeHandler(h)