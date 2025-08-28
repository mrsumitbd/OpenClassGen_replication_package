class Writer(object):
    '''Visual Studio XML tool file writer.'''

    def __init__(self, tool_file_path, name):
        '''Initializes the tool file.

        Args:
          tool_file_path: Path to the tool file.
          name: Name of the tool file.
        '''
        self.tool_file_path = tool_file_path
        self.name = name
        self._rules = []

    def AddCustomBuildRule(self, name, cmd, description,
                           additional_dependencies,
                           outputs, extensions):
        '''Adds a rule to the tool file.'''
        def _join(x):
            if isinstance(x, str) or not hasattr(x, '__iter__'):
                return x or ''
            return ';'.join(x)
        rule = {
            'Name': name or '',
            'CommandLine': cmd or '',
            'Description': description or '',
            'AdditionalDependencies': _join(additional_dependencies),
            'Outputs': _join(outputs),
            'Extensions': _join(extensions),
        }
        self._rules.append(rule)

    def WriteIfChanged(self):
        '''Writes the tool file.'''
        doc = xml.dom.minidom.Document()
        root = doc.createElement('VisualStudioToolFile')
        root.setAttribute('Name', self.name)
        doc.appendChild(root)
        for r in self._rules:
            elem = doc.createElement('CustomBuildRule')
            for attr in ('Name', 'CommandLine', 'Description',
                         'AdditionalDependencies', 'Outputs', 'Extensions'):
                elem.setAttribute(attr, r[attr])
            root.appendChild(elem)
        xml_bytes = doc.toprettyxml(indent='  ', encoding='utf-8')
        # Ensure directory exists
        d = os.path.dirname(self.tool_file_path)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        # Write only if changed
        if os.path.exists(self.tool_file_path):
            with open(self.tool_file_path, 'rb') as f:
                existing = f.read()
            if existing == xml_bytes:
                return
        with open(self.tool_file_path, 'wb') as f:
            f.write(xml_bytes)