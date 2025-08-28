class KerviLog(object):
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def info(self, message, *args):
        self.logger.info(message, *args)

    def debug(self, message, *args):
        self.logger.debug(message, *args)

    def error(self, message, *args):
        self.logger.error(message, *args)

    def exception(self, message, *args):
        self.logger.exception(message, *args)

    def fatal(self, message, *args):
        self.logger.critical(message, *args)