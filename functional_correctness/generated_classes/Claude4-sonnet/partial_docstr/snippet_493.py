class Graph(object):
    '''A directed graph that can easily be JSON serialized for visualization.

  When serializing, it generates the following fields:
    edge: The list of all serialized Edge instances.
    node: The list of all serialized Vertex instances.
  '''

    def __init__(self):
        self._vertices = {}
        self._vertex_counter = 0
        self._edges = []

    def new_vertex(self):
        '''Creates and returns a new vertex.

    Returns:
      A new Vertex instance with a unique index.
    '''
        vertex = Vertex(self._vertex_counter)
        self._vertex_counter += 1
        return vertex

    def get_vertex(self, key):
        '''Returns or Creates a Vertex mapped by key.

    Args:
      key: A string reference for a vertex.  May refer to a new Vertex in which
      case it will be created.

    Returns:
      A the Vertex mapped to by key.
    '''
        if key not in self._vertices:
            self._vertices[key] = self.new_vertex()
        return self._vertices[key]

    def add_edge(self, source, target):
        '''Returns a new edge connecting source and target vertices.

    Args:
      source: The source Vertex.
      target: The target Vertex.

    Returns:
      A new Edge linking source to target.
    '''
        edge = Edge(source, target)
        self._edges.append(edge)
        return edge

    def to_dict(self):
        '''Returns a simplified dictionary representing the Graph.

    Returns:
      A dictionary that can easily be serialized to JSON.
    '''
        return {
            'edge': [edge.to_dict() for edge in self._edges],
            'node': [vertex.to_dict() for vertex in self._vertices.values()]
        }