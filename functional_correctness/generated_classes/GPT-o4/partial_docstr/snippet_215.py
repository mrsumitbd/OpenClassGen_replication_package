class BaseDataSource(ABC):

    def __init__(self, *args, **kwargs):
        super().__init__()

    @abstractmethod
    def get_data(self):
        """Get all the data. Subclasses should override this"""
        raise NotImplementedError

    @abstractmethod
    def get_header(self):
        """Get the header - First row. Subclasses should override this"""
        raise NotImplementedError

    @abstractmethod
    def get_first_column(self):
        """
        Get the first column. Generally would be the x axis.
        Subclasses should override this
        """
        raise NotImplementedError