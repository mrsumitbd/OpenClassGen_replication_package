class NoLogger(object):
    """A logger that does nothing."""

    def info(self, *args, **kwargs):
        """Hide information messages."""
        pass

    def warning(self, *args, **kwargs):
        """Hide warning messages."""
        pass

    def severe(self, *args, **kwargs):
        """Hide severe messages."""
        pass