class LogSetup(object):
    class _ColorFormatter(logging.Formatter):
        COLOR_MAP = {
            logging.DEBUG:    '\033[36m',  # cyan
            logging.INFO:     '\033[32m',  # green
            logging.WARNING:  '\033[33m',  # yellow
            logging.ERROR:    '\033[31m',  # red
            logging.CRITICAL: '\033[41m',  # red background
        }
        RESET = '\033[0m'
        def format(self, record):
            orig_levelname = record.levelname
            color = self.COLOR_MAP.get(record.levelno, '')
            if color:
                record.levelname = f"{color}{orig_levelname}{self.RESET}"
            result = super().format(record)
            record.levelname = orig_levelname
            return result

    def __init__(self, max_size=500, max_backup=5, debug_logging=False,
                 colorized_messages=False):
        """
        Setup Logging.

        :param max_size: int
        :param max_backup: int
        :param debug_logging: bool
        :param colorized_messages: bool
        """
        self.max_size = max_size
        self.max_backup = max_backup
        self.debug_logging = debug_logging
        self.colorized = colorized_messages
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        self._plain_formatter = logging.Formatter(fmt)
        if self.colorized:
            self._color_formatter = self._ColorFormatter(fmt)
        else:
            self._color_formatter = self._plain_formatter

    def default_logger(self, name=__name__, enable_stream=False,
                       enable_file=True):
        """
        Default Logger.

        :param name: str
        :param enable_stream: bool
        :param enable_file: bool
        :return: Logger
        """
        logger = logging.getLogger(name)
        # reset handlers to avoid duplicates
        for h in list(logger.handlers):
            logger.removeHandler(h)
        logger.propagate = False
        level = logging.DEBUG if self.debug_logging else logging.INFO
        logger.setLevel(level)

        if enable_stream:
            sh = logging.StreamHandler(sys.stdout)
            self.set_handler(logger, sh)

        if enable_file:
            # sanitize name for filename
            fname = f"{name.replace('.', '_')}.log"
            path = self.return_logfile(fname)
            fh = logging.handlers.RotatingFileHandler(
                path, maxBytes=self.max_size, backupCount=self.max_backup,
                encoding='utf-8'
            )
            self.set_handler(logger, fh)

        return logger

    def set_handler(self, log, handler):
        """
        Set the logging level as well as the handlers.

        :param log: Logger
        :param handler: Handler
        """
        level = logging.DEBUG if self.debug_logging else logging.INFO
        handler.setLevel(level)
        # choose formatter
        if isinstance(handler, logging.StreamHandler) and self.colorized:
            handler.setFormatter(self._color_formatter)
        else:
            handler.setFormatter(self._plain_formatter)
        log.addHandler(handler)

    @staticmethod
    def return_logfile(filename, log_dir='/var/log'):
        """
        Return a path for logging file.

        :param filename: str
        :param log_dir: str
        :return: str
        """
        use_dir = None
        try:
            is_root = (os.geteuid() == 0)
        except AttributeError:
            is_root = False
        if is_root and os.path.isdir(log_dir):
            use_dir = log_dir
        else:
            home = os.path.expanduser("~")
            use_dir = home
        return os.path.join(use_dir, filename)