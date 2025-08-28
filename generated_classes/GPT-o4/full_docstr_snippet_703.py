class SafeParser:
    '''Safe parser for Python processes which doesn't evaluate any code.'''

    def __init__(self, source):
        '''Construct process parser.

        :param source: Process source code string
        '''
        self.source = source
        try:
            self.tree = ast.parse(source)
        except SyntaxError:
            self.tree = None

    def parse(self):
        '''Parse process.

        :return: A list of discovered process descriptors
        '''
        if self.tree is None:
            return []

        descriptors = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                bases = [self._get_base_name(b) for b in node.bases]
                methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                descriptors.append({
                    'name': node.name,
                    'bases': bases,
                    'methods': methods
                })
        return descriptors

    def base_classes(self):
        '''Parse process.

        :return: A list of the base classes for the processes.
        '''
        if self.tree is None:
            return []

        bases = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                for b in node.bases:
                    bases.add(self._get_base_name(b))
        return list(bases)

    def _get_base_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            parts = []
            while isinstance(node, ast.Attribute):
                parts.insert(0, node.attr)
                node = node.value
            if isinstance(node, ast.Name):
                parts.insert(0, node.id)
            return ".".join(parts)
        else:
            return ast.dump(node)