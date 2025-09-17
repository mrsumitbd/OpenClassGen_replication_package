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
        self.rules = []

    def AddCustomBuildRule(self, name, cmd, description,
                           additional_dependencies,
                           outputs, extensions):
        '''Adds a rule to the tool file.

        Args:
          name: Name of the rule.
          description: Description of the rule.
          cmd: Command line of the rule.
          additional_dependencies: other files which may trigger the rule.
          outputs: outputs of the rule.
          extensions: extensions handled by the rule.
        '''
        rule = {
            'name': name,
            'cmd': cmd,
            'description': description,
            'additional_dependencies': additional_dependencies,
            'outputs': outputs,
            'extensions': extensions
        }
        self.rules.append(rule)

    def WriteIfChanged(self):
        '''Writes the tool file.'''
        # Create the root element
        root = ET.Element('VisualStudioToolFile')
        root.set('Name', self.name)
        root.set('Version', '8.00')
        
        # Create Rules element
        rules_elem = ET.SubElement(root, 'Rules')
        
        # Add each custom build rule
        for rule in self.rules:
            rule_elem = ET.SubElement(rules_elem, 'CustomBuildRule')
            rule_elem.set('Name', rule['name'])
            rule_elem.set('DisplayName', rule['name'])
            rule_elem.set('CommandLine', rule['cmd'])
            rule_elem.set('Description', rule['description'])
            rule_elem.set('FileExtensions', rule['extensions'])
            rule_elem.set('AdditionalDependencies', rule['additional_dependencies'])
            rule_elem.set('Outputs', rule['outputs'])
            rule_elem.set('ExecutionDescription', rule['description'])
        
        # Convert to string with proper formatting
        rough_string = ET.tostring(root, 'unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent='  ')
        
        # Remove empty lines
        pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])
        
        # Check if file exists and content is different
        should_write = True
        if os.path.exists(self.tool_file_path):
            try:
                with open(self.tool_file_path, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
                if existing_content == pretty_xml:
                    should_write = False
            except:
                pass
        
        # Write file if changed or doesn't exist
        if should_write:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.tool_file_path), exist_ok=True)
            
            with open(self.tool_file_path, 'w', encoding='utf-8') as f:
                f.write(pretty_xml)