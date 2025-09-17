class Graph(object):
    '''A directed graph that can easily be JSON serialized for visualization.

  When serializing, it generates the following fields:
    edge: The list of all serialized Edge instances.
    node: The list of all serialized Vertex instances.
  '''

    class Vertex(object):
        def __init__(self, index, key=None):
            self.index = index
            self.key = key

        def to_dict(self):
            d = {'index': self.index}
            if self.key is not None:
                d['key'] = self.key
            return d

    class Edge(object):
        def __init__(self, source, target):
            self.source = source
            self.target = target

        def to_dict(self):
            return {
                'source': self.source.index,
                'target': self.target.index
            }

    def __init__(self):
        self._vertices = []
        self._edges = []
        self._key_map = {}
        self._next_index = 0

    def new_vertex(self):
        v = Graph.Vertex(self._next_index)
        self._next_index += 1
        self._vertices.append(v)
        return v

    def get_vertex(self, key):
        if key in self._key_map:
            return self._key_map[key]
        v = Graph.Vertex(self._next_index, key)
        self._next_index += 1
        self._vertices.append(v)
        self._key_map[key] = v
        return v

    def add_edge(self, source, target):
        e = Graph.Edge(source, target)
        self._edges.append(e)
        return e

    def to_dict(self):
        return {
            'node': [v.to_dict() for v in self._vertices],
            'edge': [e.to_dict() for e in self._edges]
        }