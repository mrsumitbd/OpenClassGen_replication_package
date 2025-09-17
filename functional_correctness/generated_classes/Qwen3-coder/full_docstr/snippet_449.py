class __Singleton(object):
    '''Singleton design pattern.'''


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
        self.models_dir = models_dir
        self.data_dir = data_dir
        self.logs_dir = logs_dir


    def mkdir_p(self, path):
        '''Recursively create directories.'''
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise