class ConfigValidator(object):
    '''ConfigValidator

    Attributes:
        cp: An class which fulfill the configparser interface
        cp_init_args: This item will be passed as kwargs to new cp instances
        data: local data store

    '''

    def __init__(self, cp, cp_init_args=None):
        '''Inits ConfigValidator.'''
        self.cp = cp
        self.cp_init_args = cp_init_args or {}
        self.data = {}

    def add_data(self, key, value):
        '''
        Add data to the local data store
        '''
        self.data[key] = value

    def remove_data(self, key):
        '''
        Remove data from the local data store
        '''
        if key in self.data:
            del self.data[key]

    def parse(self, config_dict, feature_key="__feature__"):
        '''

        :param config_dict:
        :param feature_key:
        :return:
        '''
        # Create a new instance of the configparser class
        config_parser = self.cp(**self.cp_init_args)
        
        # Process the config_dict to handle feature-specific configurations
        processed_config = {}
        
        for section, options in config_dict.items():
            if isinstance(options, dict):
                # Handle regular sections
                processed_config[section] = {}
                for option, value in options.items():
                    if option == feature_key and isinstance(value, list):
                        # Handle feature-specific configurations
                        for feature_config in value:
                            if isinstance(feature_config, dict):
                                for feat_section, feat_options in feature_config.items():
                                    if feat_section not in processed_config:
                                        processed_config[feat_section] = {}
                                    processed_config[feat_section].update(feat_options)
                    else:
                        processed_config[section][option] = value
            else:
                # Handle top-level options
                processed_config[section] = options
        
        # Return the processed configuration
        return processed_config