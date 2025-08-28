class SafeParser:
    '''Safe parser for Python processes which doesn't evaluate any code.'''

    def __init__(self, source):
        '''Construct process parser.

        :param source: Process source code string
        '''
        self.source = source
        self._tree = ast.parse(source)

    def parse(self):
        '''Parse process.

        :return: A list of discovered process descriptors
        '''
        descriptors = []
        for node in ast.walk(self._tree):
            if isinstance(node, ast.ClassDef):
                name = node.name
                bases = [self._get_base_name(b) for b in node.bases]
                descriptors.append({
                    'name': name,
                    'bases': bases,
                    'lineno': node.lineno,
                })
        return descriptors

    def base_classes(self):
        '''Parse process.

        :return: A list of the base classes for the processes.
        '''
        return [desc['bases'] for desc in self.parse()]

    def _get_base_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            return self._get_attribute_name(node)
        if isinstance(node, ast.Subscript):
            return self._get_base_name(node.value)
        if isinstance(node, ast.Call):
            return self._get_base_name(node.func)
        return ast.dump(node)

    def _get_attribute_name(self, node):
        parts = []
        while isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.append(node.id)
        return '.'.join(reversed(parts))