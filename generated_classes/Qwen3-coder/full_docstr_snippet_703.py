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
                # Check if this class inherits from a Process class
                base_classes = self._get_base_classes(node)
                if self._is_process_class(base_classes):
                    process_descriptor = {
                        'name': node.name,
                        'bases': base_classes,
                        'methods': self._get_methods(node),
                        'attributes': self._get_attributes(node)
                    }
                    self.processes.append(process_descriptor)
        
        return self.processes

    def base_classes(self):
        '''Parse process.

        :return: A list of the base classes for the processes.
        '''
        processes = self.parse()
        all_base_classes = []
        
        for process in processes:
            all_base_classes.extend(process['bases'])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_base_classes = []
        for base_class in all_base_classes:
            if base_class not in seen:
                seen.add(base_class)
                unique_base_classes.append(base_class)
        
        return unique_base_classes

    def _get_base_classes(self, class_node):
        '''Extract base classes from a class definition node.'''
        bases = []
        for base in class_node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                # Handle cases like module.Class
                bases.append(self._get_attribute_name(base))
            elif isinstance(base, ast.Call):
                # Handle cases like SomeClass()
                if isinstance(base.func, ast.Name):
                    bases.append(base.func.id)
                elif isinstance(base.func, ast.Attribute):
                    bases.append(self._get_attribute_name(base.func))
        return bases

    def _get_attribute_name(self, attr_node):
        '''Extract full attribute name (e.g., module.Class).'''
        if isinstance(attr_node, ast.Name):
            return attr_node.id
        elif isinstance(attr_node, ast.Attribute):
            return f"{self._get_attribute_name(attr_node.value)}.{attr_node.attr}"
        return ""

    def _is_process_class(self, base_classes):
        '''Determine if a class is a process class based on its base classes.'''
        process_indicators = ['Process', 'BaseProcess', 'multiprocessing.Process']
        for base in base_classes:
            if any(indicator in base for indicator in process_indicators):
                return True
        return False

    def _get_methods(self, class_node):
        '''Extract method names from a class definition.'''
        methods = []
        for item in class_node.body:
            if isinstance(item, ast.FunctionDef):
                methods.append(item.name)
        return methods

    def _get_attributes(self, class_node):
        '''Extract attribute names from a class definition.'''
        attributes = []
        for item in class_node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.append(target.id)
            elif isinstance(item, ast.AnnAssign):
                if isinstance(item.target, ast.Name):
                    attributes.append(item.target.id)
        return attributes