class Path(object):
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.nodes = [start_node]
        self.g_cost = 0
        
    def calc_f_val(self, node):
        g_val = self.g_cost
        h_val = abs(node.x - self.end_node.x) + abs(node.y - self.end_node.y)
        return g_val + h_val