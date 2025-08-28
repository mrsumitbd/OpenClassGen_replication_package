class LogSetup(object):

    def __init__(self, max_size=500, max_backup=5, debug_logging=False,
                 colorized_messages=False):
        '''Setup Logging.

        :param max_size: ``int``
        :param max_backup: ``int``
        :param debug_logging: ``bol``
        :param colorized_messages: ``bol``
        '''
        self.max_size = max_size * 1024 * 1024  # Convert MB to bytes
        self.max_backup = max_backup
        self.debug_logging = debug_logging
        self.colorized_messages = colorized_messages

    def default_logger(self, name=__name__, enable_stream=False,
                       enable_file=True):
        '''Default Logger.

        This is set to use a rotating File handler and a stream handler.
        If you use this logger all logged output that is INFO and above will
        be logged, unless debug_logging is set then everything is logged.
        The logger will send the same data to a stdout as it does to the
        specified log file.

        You can disable the default handlers by setting either `enable_file` or
        `enable_stream` to `False`

        :param name: ``str``
        :param enable_stream: ``bol``
        :param enable_file: ``bol``
        :return: ``object``
        '''
        log = logging.getLogger(name)
        
        # Clear any existing handlers
        log.handlers = []
        
        # Set logging level
        if self.debug_logging:
            log.setLevel(logging.DEBUG)
        else:
            log.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Add file handler if enabled
        if enable_file:
            logfile = self.return_logfile(f"{name}.log")
            file_handler = logging.handlers.RotatingFileHandler(
                logfile, maxBytes=self.max_size, backupCount=self.max_backup
            )
            file_handler.setFormatter(formatter)
            self.set_handler(log, file_handler)
        
        # Add stream handler if enabled
        if enable_stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.set_handler(log, stream_handler)
        
        return log

    def set_handler(self, log, handler):
        '''Set the logging level as well as the handlers.

        :param log: ``object``
        :param handler: ``object``
        '''
        if self.debug_logging:
            handler.setLevel(logging.DEBUG)
        else:
            handler.setLevel(logging.INFO)
        
        log.addHandler(handler)

    @staticmethod
    def return_logfile(filename, log_dir='/var/log'):
        '''Return a path for logging file.

        If ``log_dir`` exists and the userID is 0 the log file will be written
        to the provided log directory. If the UserID is not 0 or log_dir does
        not exist the log file will be written to the users home folder.

        :param filename: ``str``
        :param log_dir: ``str``
        :return: ``str``
        '''
        try:
            user_id = os.geteuid()
        except AttributeError:
            # Windows doesn't have geteuid
            user_id = 0 if os.name == 'nt' else 1000
            
        if user_id == 0 and os.path.exists(log_dir):
            return os.path.join(log_dir, filename)
        else:
            home_dir = os.path.expanduser('~')
            return os.path.join(home_dir, filename)