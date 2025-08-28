class DevNull:
    '''
    DevNull class that has a no-op write and flush method.
    '''

    def write(self, *args, **kwargs):
        return None

    def flush(self):
        return None