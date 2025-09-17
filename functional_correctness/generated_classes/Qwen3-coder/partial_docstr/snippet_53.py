class StructuredLogger(metaclass=abc.ABCMeta):
    '''
    ABSTRACT BASE CLASS FOR JSON LOGGING
    '''

    @abc.abstractmethod
    def write(self, template, params):
        pass

    @abc.abstractmethod
    def stop(self):
        pass