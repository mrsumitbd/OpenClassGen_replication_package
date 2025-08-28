class CustomLogger:
    '''Helper Logger to redirect STDOUT or STDERR to a logging hander.

    It wraps a Logger class into a file like object, which provides a handy
    way to redirect STDOUT or STDERR to a logger. This class provides the
    necessary methods (write, flush and close) to build a file-like object
    and it can not be used directly as it does not provide a logging handler.
    Instead, you must instantiate one of subclass (CustomRotatingFileLogger and
    CustomUdpLogger).

    Arguments
        handler (int): A logging handler to use.

    Methods:
        write(string): Write string to logger with newlines removed.
        flush(): Flushe logger messages.
        close(): Close logger.

    Returns:
        A logger object.

    '''

    def __init__(self, handler):
        '''Create a logging.Logger class with extended functionality.'''
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

    def write(self, string):
        '''Erase newline from a string and write to the logger.'''
        if string.strip():
            self.logger.info(string.rstrip('\n\r'))

    def flush(self):
        '''Flush logger's data.'''
        for handler in self.logger.handlers:
            handler.flush()

    def close(self):
        '''Call the closer method of the logger.'''
        for handler in self.logger.handlers:
            handler.close()