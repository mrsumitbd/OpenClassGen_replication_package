class StdErrForwarder(object):
    '''
    Used to forward content to the current sys.stdout. This allows for rebinding sys.stdout without
    remapping associations in loggers
    '''

    def write(self, content):
        sys.stdout.write(content)

    def flush(self):
        sys.stdout.flush()

    def isatty(self):
        return getattr(sys.stdout, 'isatty', lambda: False)()