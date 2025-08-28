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
        
        # Parse the XML from the stream
        tree = ET.parse(stream)
        root = tree.getroot()
        
        # Parse metadata
        metadata_element = root.find('metadata')
        if metadata_element is not None:
            for child in metadata_element:
                definition.metadata[child.tag] = child.text
        
        # Parse inputs
        inputs_element = root.find('inputs')
        if inputs_element is not None:
            for input_element in inputs_element.findall('input'):
                name = input_element.get('name')
                if name is not None:
                    params = {}
                    for param in input_element:
                        params[param.tag] = param.text
                    definition.inputs[name] = params
        
        return definition