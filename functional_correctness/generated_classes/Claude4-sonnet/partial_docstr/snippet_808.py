class SafeParser:
    '''Safe parser for Python processes which doesn't evaluate any code.'''

    def __init__(self, source):
        '''Construct process parser.

        :param source: Process source code string
        '''
        self.source = source
        self.tree = None
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
        
        processes = []
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                process_info = {
                    'name': node.name,
                    'lineno': node.lineno,
                    'bases': [self._get_base_name(base) for base in node.bases],
                    'methods': [],
                    'attributes': []
                }
                
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        method_info = {
                            'name': item.name,
                            'lineno': item.lineno,
                            'args': [arg.arg for arg in item.args.args]
                        }
                        process_info['methods'].append(method_info)
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                process_info['attributes'].append(target.id)
                
                processes.append(process_info)
        
        return processes

    def base_classes(self):
        '''Parse process.

        :return: A list of the base classes for the processes.
        '''
        if self.tree is None:
            return []
        
        base_classes = set()
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    base_name = self._get_base_name(base)
                    if base_name:
                        base_classes.add(base_name)
        
        return list(base_classes)
    
    def _get_base_name(self, base_node):
        '''Extract base class name from AST node.'''
        if isinstance(base_node, ast.Name):
            return base_node.id
        elif isinstance(base_node, ast.Attribute):
            parts = []
            node = base_node
            while isinstance(node, ast.Attribute):
                parts.append(node.attr)
                node = node.value
            if isinstance(node, ast.Name):
                parts.append(node.id)
            return '.'.join(reversed(parts))
        return None