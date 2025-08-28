class ConfigValidator(object):
    '''ConfigValidator

    Attributes:
        cp: A class which fulfills the configparser interface
        cp_init_args: This item will be passed as kwargs to new cp instances
        data: local data store
    '''

    def __init__(self, cp, cp_init_args=None):
        '''Inits ConfigValidator.'''
        self.cp = cp
        self.cp_init_args = cp_init_args.copy() if cp_init_args else {}
        self.data = {}

    def add_data(self, key, value):
        '''Add a data item to the local store.'''
        self.data[key] = value

    def remove_data(self, key):
        '''Remove a data item from the local store.'''
        del self.data[key]

    def parse(self, config_dict, feature_key="__feature__"):
        '''
        Build and return a configparser instance filled with the provided
        config_dict plus any locally stored data under the feature_key section.
        '''
        cfg = self.cp(**self.cp_init_args)
        # build a copy of the input dict
        merged = {}
        for section, opts in config_dict.items():
            merged[section] = opts.copy() if isinstance(opts, dict) else opts
        # inject feature data if available
        if self.data:
            merged[feature_key] = self.data.copy()
        cfg.read_dict(merged)
        return cfg