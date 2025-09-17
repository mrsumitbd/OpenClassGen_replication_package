class Node:

    def __init__(self, name, path=()):
        '''
            Initialize self with "name" string and the tuple "path" of its parents.
            "self" is added to the tuple as its last item.
        '''
        self.name = name
        self.path = path + (self,)

    def get_full_name(self):
        '''
            A `no-member` message was emitted:
            nodes.py:17:24: E1101: Instance of 'tuple' has no '__name' member (no-member)
        '''
        return '.'.join(node.name for node in self.path)