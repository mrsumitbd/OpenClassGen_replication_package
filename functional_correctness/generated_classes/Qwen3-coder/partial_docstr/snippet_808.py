class SafeParser:
    '''Safe parser for Python processes which doesn't evaluate any code.'''

    def __init__(self, source):
        '''Construct process parser.

        :param source: Process source code string
        '''
        self.source = source
        self.tree = ast.parse(source)
        self.processes = []

    def parse(self):
        '''Parse process.

        :return: A list of discovered process descriptors
        '''
        self.processes = []
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                # Check if class inherits from a base class (likely a process)
                if node.bases:
                    process_descriptor = {
                        'name': node.name,
                        'bases': [ast.unparse(base) for base in node.bases],
                        'lineno': node.lineno,
                        'methods': []
                    }
                    
                    # Extract methods
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef):
                            method_info = {
                                'name': item.name,
                                'lineno': item.lineno,
                                'args': [arg.arg for arg in item.args.args]
                            }
                            process_descriptor['methods'].append(method_info)
                    
                    self.processes.append(process_descriptor)
        
        return self.processes

    def base_classes(self):
        '''Parse process.

        :return: A list of the base classes for the processes.
        '''
        base_classes = set()
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                for base in node.bases:
                    base_classes.add(ast.unparse(base))
        
        return list(base_classes)