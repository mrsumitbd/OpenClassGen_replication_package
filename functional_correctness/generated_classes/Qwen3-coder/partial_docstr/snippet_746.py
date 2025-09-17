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
        self.handler = handler

    def write(self, string):
        '''Erase newline from a string and write to the logger.'''
        if string.strip():  # Only write non-empty strings
            self.handler.write(string.rstrip('\n'))

    def flush(self):
        '''Flush logger's data.'''
        if hasattr(self.handler, 'flush'):
            self.handler.flush()

    def close(self):
        '''Call the closer method of the logger.'''
        if hasattr(self.handler, 'close'):
            self.handler.close()