class StructuredLogger(ABC):
    '''
    ABSTRACT BASE CLASS FOR JSON LOGGING
    '''

    @abstractmethod
    def write(self, template, params):
        pass

    @abstractmethod
    def stop(self):
        pass