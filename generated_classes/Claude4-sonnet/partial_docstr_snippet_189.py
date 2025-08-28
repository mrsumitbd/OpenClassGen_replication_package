class DevNull:
    '''
    DevNull class that has a no-op write and flush method.
    '''

    def write(self, *args, **kwargs):
        pass

    def flush(self):
        pass