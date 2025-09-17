class InputDefinition:
    '''``InputDefinition`` encodes the XML defining inputs that Splunk passes to
    a modular input script.

     **Example**::

        i = InputDefinition()

    '''

    def __init__(self):
        self.name = None
        self.stanza = None
        self.server_host = None
        self.server_uri = None
        self.checkpoint_dir = None
        self.session_key = None
        self.metadata = {}
        self.parameters = {}

    def __eq__(self, other):
        if not isinstance(other, InputDefinition):
            return False
        return (
            self.name == other.name and
            self.stanza == other.stanza and
            self.server_host == other.server_host and
            self.server_uri == other.server_uri and
            self.checkpoint_dir == other.checkpoint_dir and
            self.session_key == other.session_key and
            self.metadata == other.metadata and
            self.parameters == other.parameters
        )

    @staticmethod
    def parse(stream):
        '''Parse a stream containing XML into an ``InputDefinition``.

        :param stream: stream containing XML to parse.
        :return: definition: an ``InputDefinition`` object.
        '''
        import xml.etree.ElementTree as ET
        root = ET.parse(stream).getroot()
        definition = InputDefinition()
        definition.server_host = root.findtext('server_host')
        definition.server_uri = root.findtext('server_uri')
        definition.checkpoint_dir = root.findtext('checkpoint_dir')
        definition.session_key = root.findtext('session_key')
        config = root.find('configuration')
        if config is not None:
            stanza = config.find('stanza')
            if stanza is not None:
                definition.stanza = stanza.get('name')
                definition.name = stanza.get('name')
                for element in stanza:
                    if element.tag == 'param':
                        definition.parameters[element.get('name')] = element.text or ''
                    elif element.tag == 'meta':
                        definition.metadata[element.get('name')] = element.text or ''
        return definition