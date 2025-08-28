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
        pass

    def _visit_one(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def visit(self, obj):
        '''Visit a node or a list of nodes. Other values are ignored'''
        if hasattr(obj, '__iter__') and not isinstance(obj, str):
            for item in obj:
                self.visit(item)
        elif hasattr(obj, '__class__'):
            self._visit_one(obj)