class node:
    '''!
    @brief Represents a node in a KD-Tree.
    @details The KD-Tree node contains point's coordinates, discriminator, payload and pointers to parent and children.

    @see kdtree_balanced
    @see kdtree

    '''

    def __init__(self, data=None, payload=None, left=None, right=None, disc=None, parent=None):
        '''!
            @brief Creates KD-tree node.

            @param[in] data (list): Data point that is presented as list of coordinates.
            @param[in] payload (any): Payload of node (pointer to essence that is attached to this node).
            @param[in] left (node): Node of KD-Tree that represents left successor.
            @param[in] right (node): Node of KD-Tree that represents right successor.
            @param[in] disc (uint): Index of dimension of that node.
            @param[in] parent (node): Node of KD-Tree that represents parent.

        '''
        self.data = data
        self.payload = payload
        self.left = left
        self.right = right
        self.disc = disc
        self.parent = parent

    def __repr__(self):
        '''!
            @return (string) Default representation of the node.
        '''
        return f"node(data={self.data!r}, payload={self.payload!r}, disc={self.disc!r})"

    def __str__(self):
        '''!
            @return (string) String representation of the node.
        '''
        return f"KDNode at dim {self.disc} with data {self.data}"

    def get_children(self):
        '''!
            @brief Returns list of not `None` children of the node.

            @return (list) list of not `None` children of the node; if the node does not have children
                            then `None` is returned.

        '''
        children = [child for child in (self.left, self.right) if child is not None]
        return children if children else None