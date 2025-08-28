class MetadataDictBase:
    '''Class used to parse metadata from kwargs'''

    def __init__(self, metadata_dict):
        '''Initialize local variables'''
        self.metadata_dict = metadata_dict

    def __getattr__(self, key):
        '''Return item from metadata in case of unknown attribute'''
        if key in self.metadata_dict:
            return self.metadata_dict[key]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")