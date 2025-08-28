class __Singleton(object):
    '''Singleton design pattern.'''
    _instance = None

    def __new__(cls, models_dir='models/', data_dir='data/', logs_dir='logs/'):
        if cls._instance is None:
            cls._instance = super(__Singleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, models_dir='models/', data_dir='data/',
                 logs_dir='logs/'):
        '''Constructor.

        Parameters
        ----------
        models_dir : string, optional (default='models/')
            directory path to store trained models.
            Path is relative to ~/.yadlt
        data_dir : string, optional (default='data/')
            directory path to store model generated data.
            Path is relative to ~/.yadlt
        logs_dir : string, optional (default='logs/')
            directory path to store yadlt and tensorflow logs.
            Path is relative to ~/.yadlt
        '''
        if getattr(self, '_initialized', False):
            return

        config_root = os.path.join(os.path.expanduser('~'), '.yadlt')
        self.mkdir_p(config_root)

        self.models_dir = os.path.join(config_root, models_dir)
        self.data_dir   = os.path.join(config_root, data_dir)
        self.logs_dir   = os.path.join(config_root, logs_dir)

        self.mkdir_p(self.models_dir)
        self.mkdir_p(self.data_dir)
        self.mkdir_p(self.logs_dir)

        self._initialized = True

    def mkdir_p(self, path):
        '''Recursively create directories.'''
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise