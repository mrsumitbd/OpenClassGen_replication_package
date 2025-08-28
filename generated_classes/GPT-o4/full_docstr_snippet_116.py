class BaseResponseItem(object):
    '''
    Base class for responses from DDSConnection API converts dict into properties for subclasses.
    '''
    def __init__(self, dds_connection, data_dict):
        '''
        :param dds_connection: DDSConnection
        :param data_dict: dict: dictionary response from DDSConnection API
        '''
        self._dds_connection = dds_connection
        self._data = data_dict or {}

    def __getattr__(self, key):
        '''
        Return property from the dictionary passed to the constructor.
        '''
        if key in self._data:
            return self._data[key]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")