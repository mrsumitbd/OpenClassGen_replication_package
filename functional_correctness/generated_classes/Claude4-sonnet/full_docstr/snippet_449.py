class __Singleton(object):
    '''Singleton design pattern.'''
    
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
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
        if not self._initialized:
            self.home_dir = os.path.expanduser('~/.yadlt/')
            self.models_dir = os.path.join(self.home_dir, models_dir)
            self.data_dir = os.path.join(self.home_dir, data_dir)
            self.logs_dir = os.path.join(self.home_dir, logs_dir)
            
            self.mkdir_p(self.home_dir)
            self.mkdir_p(self.models_dir)
            self.mkdir_p(self.data_dir)
            self.mkdir_p(self.logs_dir)
            
            self._initialized = True

    def mkdir_p(self, path):
        '''Recursively create directories.'''
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise