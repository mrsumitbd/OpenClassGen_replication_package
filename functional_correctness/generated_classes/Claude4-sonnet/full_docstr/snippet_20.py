class AlignakObject(object):
    '''This class provides a generic way to instantiate alignak objects.
    Attributes are serialized dynamically, whether we un-serialize
    them create them at run / parsing time

    '''

    properties = {}
    
    def __init__(self, params=None, parsing=True):
        '''
        If parsing is True, then the objects are created from an initial configuration
        read by the Alignak arbiter else the objects are restored from a previously
        serialized instance sent by the arbiter to another daemon.

        This function checks the object uuid in the following manner:
        - in parsing mode, this function simply creates an object uuid
        - in non parsing mode, this function restore the object attributes from the provided params

        :param params: initialization parameters
        :type params: dict
        :param parsing: configuration parsing phase
        :type parsing: bool
        '''
        if params is None:
            params = {}
            
        if parsing:
            self.uuid = str(uuid.uuid4())
            for key, value in params.items():
                setattr(self, key, value)
        else:
            for key, value in params.items():
                setattr(self, key, value)
            if not hasattr(self, 'uuid'):
                self.uuid = str(uuid.uuid4())

    def serialize(self, no_json=True, printing=False):
        '''This function serializes into a simple dictionary object.

        It is used when transferring data to other daemons over the network (http)

        Here is the generic function that simply export attributes declared in the
        properties dictionary of the object.

        :return: Dictionary containing key and value from properties
        :rtype: dict
        '''
        result = {}
        
        # Always include uuid
        if hasattr(self, 'uuid'):
            result['uuid'] = self.uuid
            
        # Serialize properties defined in the properties dictionary
        for prop_name in getattr(self.__class__, 'properties', {}):
            if hasattr(self, prop_name):
                value = getattr(self, prop_name)
                result[prop_name] = value
                
        # Serialize any other attributes not in properties
        for attr_name in dir(self):
            if not attr_name.startswith('_') and attr_name != 'uuid':
                if attr_name not in getattr(self.__class__, 'properties', {}):
                    if not callable(getattr(self, attr_name)):
                        result[attr_name] = getattr(self, attr_name)
        
        if no_json:
            return result
        else:
            return json.dumps(result)

    def fill_default(self):
        '''
        Define the object properties with a default value when the property is not yet defined

        :return: None
        '''
        properties = getattr(self.__class__, 'properties', {})
        for prop_name, prop_config in properties.items():
            if not hasattr(self, prop_name):
                if isinstance(prop_config, dict) and 'default' in prop_config:
                    setattr(self, prop_name, prop_config['default'])
                elif isinstance(prop_config, tuple) and len(prop_config) > 1:
                    setattr(self, prop_name, prop_config[1])