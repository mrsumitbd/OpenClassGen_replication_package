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
        self.cp_init_args = cp_init_args if cp_init_args is not None else {}
        self.data = {}

    def add_data(self, key, value):
        '''
        TODO
        '''
        self.data[key] = value

    def remove_data(self, key):
        '''
        TODO
        '''
        if key in self.data:
            del self.data[key]

    def parse(self, config_dict, feature_key="__feature__"):
        '''

        :param config_dict:
        :param feature_key:
        :return:
        '''
        parser = self.cp(**self.cp_init_args)
        
        for section_name, section_data in config_dict.items():
            if isinstance(section_data, dict):
                parser.add_section(section_name)
                for key, value in section_data.items():
                    if key != feature_key:
                        parser.set(section_name, key, str(value))
        
        return parser