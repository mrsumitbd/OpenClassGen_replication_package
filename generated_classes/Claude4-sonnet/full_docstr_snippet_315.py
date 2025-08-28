class MetadataDictBase:
    '''Class used to parse metadata from kwargs'''

    def __init__(self, metadata_dict):
        '''Initialize local variables'''
        self._metadata_dict = metadata_dict or {}

    def __getattr__(self, key):
        '''Return item from metadata in case of unknown attribute'''
        if key in self._metadata_dict:
            return self._metadata_dict[key]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")