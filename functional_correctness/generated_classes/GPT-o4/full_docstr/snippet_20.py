class AlignakObject(object):
    '''This class provides a generic way to instantiate alignak objects.
    Attributes are serialized dynamically, whether we un-serialize
    them create them at run / parsing time
    '''

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
        if parsing:
            self.uuid = str(uuid.uuid4())
        else:
            if not isinstance(params, dict):
                raise ValueError("params must be a dict when parsing is False")
            for key, value in params.items():
                setattr(self, key, value)
            if not hasattr(self, 'uuid'):
                self.uuid = str(uuid.uuid4())
        # Ensure a properties dict exists (can be overridden in subclasses)
        self.properties = getattr(self, 'properties', {})
        self.fill_default()

    def serialize(self, no_json=True, printing=False):
        '''This function serializes into a simple dictionary object.

            It is used when transferring data to other daemons over the network (http)

            Here is the generic function that simply export attributes declared in the
            properties dictionary of the object.

            :return: Dictionary containing key and value from properties
            :rtype: dict
        '''
        data = {}
        for prop in self.properties:
            if hasattr(self, prop):
                data[prop] = getattr(self, prop)
        data['uuid'] = self.uuid
        if printing:
            print(data)
        if no_json:
            return data
        return json.dumps(data)

    def fill_default(self):
        '''
            Define the object properties with a default value when the property is not yet defined

            :return: None
        '''
        for prop, default in self.properties.items():
            if not hasattr(self, prop):
                setattr(self, prop, default)