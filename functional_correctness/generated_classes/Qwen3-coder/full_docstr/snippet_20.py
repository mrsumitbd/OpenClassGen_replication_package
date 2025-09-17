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
            # Create a new UUID for parsing mode
            self.uuid = str(uuid.uuid4())
            # Set attributes from params
            for key, value in params.items():
                setattr(self, key, value)
            # Fill default values for missing properties
            self.fill_default()
        else:
            # Restore attributes from params in non-parsing mode
            for key, value in params.items():
                setattr(self, key, value)

    def serialize(self, no_json=True, printing=False):
        '''This function serializes into a simple dictionary object.

        It is used when transferring data to other daemons over the network (http)

        Here is the generic function that simply export attributes declared in the
        properties dictionary of the object.

        :return: Dictionary containing key and value from properties
        :rtype: dict
        '''
        result = {}
        # Serialize attributes that are declared in properties
        for prop_name in self.properties:
            if hasattr(self, prop_name):
                result[prop_name] = getattr(self, prop_name)
        
        # Always include uuid if it exists
        if hasattr(self, 'uuid'):
            result['uuid'] = self.uuid
            
        return result

    def fill_default(self):
        '''
        Define the object properties with a default value when the property is not yet defined

        :return: None
        '''
        for prop_name, prop_info in self.properties.items():
            if not hasattr(self, prop_name):
                # Get default value from property info, default to None if not specified
                default_value = prop_info.get('default', None)
                setattr(self, prop_name, default_value)