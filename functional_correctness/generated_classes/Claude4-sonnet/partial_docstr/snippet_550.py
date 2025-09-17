class InputDefinition:
    '''``InputDefinition`` encodes the XML defining inputs that Splunk passes to
    a modular input script.

     **Example**::

        i = InputDefinition()

    '''

    def __init__(self):
        self.metadata = {}
        self.inputs = {}

    def __eq__(self, other):
        if not isinstance(other, InputDefinition):
            return False
        return self.metadata == other.metadata and self.inputs == other.inputs

    @staticmethod
    def parse(stream):
        '''Parse a stream containing XML into an ``InputDefinition``.

        :param stream: stream containing XML to parse.
        :return: definition: an ``InputDefinition`` object.
        '''
        definition = InputDefinition()
        
        tree = ET.parse(stream)
        root = tree.getroot()
        
        # Parse metadata
        configuration = root.find('configuration')
        if configuration is not None:
            for stanza in configuration.findall('stanza'):
                stanza_name = stanza.get('name')
                if stanza_name:
                    definition.metadata[stanza_name] = {}
                    for param in stanza.findall('param'):
                        param_name = param.get('name')
                        param_value = param.text if param.text else ''
                        if param_name:
                            definition.metadata[stanza_name][param_name] = param_value
        
        # Parse inputs
        for item in root.findall('item'):
            item_name = item.get('name')
            if item_name:
                definition.inputs[item_name] = {}
                for param in item.findall('param'):
                    param_name = param.get('name')
                    param_value = param.text if param.text else ''
                    if param_name:
                        definition.inputs[item_name][param_name] = param_value
        
        return definition