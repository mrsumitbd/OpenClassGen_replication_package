class StdErrForwarder(object):
    '''
    Used to forward content to the current sys.stdout. This allows for rebinding sys.stdout without
    remapping associations in loggers
    '''

    def write(self, content):
        sys.stderr.write(content)

    def flush(self):
        sys.stderr.flush()

    def isatty(self):
        return sys.stderr.isatty()