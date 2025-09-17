class Path(object):
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node

    def calc_f_val(self, node):
        sx, sy = self.start_node.state
        nx, ny = node.state
        ex, ey = self.end_node.state
        g = abs(nx - sx) + abs(ny - sy)
        h = abs(ex - nx) + abs(ey - ny)
        return g + h