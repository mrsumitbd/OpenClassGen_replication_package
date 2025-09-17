class Visitor:
    '''
    A node visitor base class that does a traversal
    of the abstract syntax tree.

    This class is meant to be subclassed, with the subclass adding
    visitor methods. The visitor method should call ``self.generic_visit(node)``
    to continue the traversal; this allows to perform arbitrary
    actions both before and after traversing the children of a node.

    The visitor methods for the nodes are ``'visit_'`` +
    class name of the node.  So a `Try` node visit function would
    be `visit_Try`.
    '''

    def generic_visit(self, node):
        '''Called if no explicit visitor function exists for a node.'''
        # Traverse all fields named in _fields
        for field in getattr(node, '_fields', ()):
            value = getattr(node, field, None)
            if isinstance(value, list):
                for item in value:
                    if hasattr(item, '__class__'):
                        self.visit(item)
            elif hasattr(value, '__class__'):
                self.visit(value)

    def _visit_one(self, node):
        # Only visit if it's a node-like object
        if node is None or not hasattr(node, '__class__'):
            return
        # Look for a method named visit_<ClassName>
        method = getattr(self, 'visit_' + node.__class__.__name__, None)
        if method is None:
            return self.generic_visit(node)
        return method(node)

    def visit(self, obj):
        '''Visit a node or a list of nodes. Other values are ignored'''
        if isinstance(obj, list):
            for node in obj:
                self._visit_one(node)
        else:
            self._visit_one(obj)