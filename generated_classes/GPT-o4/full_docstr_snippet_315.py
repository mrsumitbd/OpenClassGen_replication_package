class MetadataDictBase:
    '''Class used to parse metadata from kwargs'''

    def __init__(self, metadata_dict):
        '''Initialize local variables'''
        if metadata_dict is None:
            metadata_dict = {}
        if not isinstance(metadata_dict, dict):
            raise TypeError("metadata_dict must be a dict")
        self._metadata = metadata_dict

    def __getattr__(self, key):
        '''Return item from metadata in case of unknown attribute'''
        if key in self._metadata:
            return self._metadata[key]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")