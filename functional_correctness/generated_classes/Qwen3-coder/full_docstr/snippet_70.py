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
        root.set('Version', '8.00')
        root.set('Name', self.name)
        
        # Create the Rules element
        rules_element = ET.SubElement(root, 'Rules')
        
        # Add each rule
        for rule in self.rules:
            rule_element = ET.SubElement(rules_element, 'Rule')
            rule_element.set('Name', rule['name'])
            rule_element.set('FriendlyName', rule['name'])
            rule_element.set('Description', rule['description'])
            
            # Add additional dependencies
            if rule['additional_dependencies']:
                rule_element.set('AdditionalDependencies', rule['additional_dependencies'])
            
            # Add outputs
            if rule['outputs']:
                rule_element.set('Outputs', rule['outputs'])
            
            # Add extensions
            if rule['extensions']:
                rule_element.set('FileExtensions', rule['extensions'])
            
            # Add command
            if rule['cmd']:
                cmd_element = ET.SubElement(rule_element, 'ExecutionDescription')
                cmd_element.text = rule['cmd']
        
        # Format the XML
        rough_string = ET.tostring(root, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        formatted_xml = reparsed.toprettyxml(indent="  ", encoding='utf-8')
        
        # Remove empty lines
        lines = [line for line in formatted_xml.decode('utf-8').split('\n') if line.strip()]
        formatted_xml = '\n'.join(lines).encode('utf-8')
        
        # Write to file if content has changed
        if not os.path.exists(self.tool_file_path):
            with open(self.tool_file_path, 'wb') as f:
                f.write(formatted_xml)
            return True
        else:
            with open(self.tool_file_path, 'rb') as f:
                existing_content = f.read()
            if existing_content != formatted_xml:
                with open(self.tool_file_path, 'wb') as f:
                    f.write(formatted_xml)
                return True
        return False