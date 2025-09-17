class KerviLog(object):

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message, *args):
        msg = message % args if args else message
        self.logger.info(msg)

    def debug(self, message, *args):
        msg = message % args if args else message
        self.logger.debug(msg)

    def error(self, message, *args):
        msg = message % args if args else message
        self.logger.error(msg)

    def exception(self, message, *args):
        msg = message % args if args else message
        self.logger.exception(msg)

    def fatal(self, message, *args):
        msg = message % args if args else message
        self.logger.fatal(msg)