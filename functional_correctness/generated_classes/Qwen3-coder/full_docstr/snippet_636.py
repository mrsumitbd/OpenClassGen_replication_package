class Node:
    '''Base class for operations and leaf nodes'''

    def __and__(self, other):
        '''And operation with "&" operator'''
        return AndNode(self, other)

    def __or__(self, other):
        '''Or operation with "|" operator'''
        return OrNode(self, other)

    def eval(self, collection: 'PgCollection'):
        '''Operations and leaf nodes should implement it'''
        raise NotImplementedError("Subclasses must implement eval method")