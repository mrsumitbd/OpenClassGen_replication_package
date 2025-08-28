class Node(ABC):
    '''Base class for operations and leaf nodes'''

    def __and__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return And(self, other)

    def __rand__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return And(other, self)

    def __or__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return Or(self, other)

    def __ror__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return Or(other, self)

    @abstractmethod
    def eval(self, collection: 'PgCollection'):
        '''Operations and leaf nodes should implement it'''
        raise NotImplementedError