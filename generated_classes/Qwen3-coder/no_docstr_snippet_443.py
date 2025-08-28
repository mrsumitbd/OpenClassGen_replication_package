class Path(object):
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node
        self.nodes = [start_node]
        self.g_cost = 0
        self.h_cost = 0
        self.f_cost = 0

    def calc_f_val(self, node):
        # Calculate g_cost (distance from start to current node)
        g_cost = self.calculate_g_cost(node)
        
        # Calculate h_cost (heuristic distance from current node to end)
        h_cost = self.calculate_h_cost(node)
        
        # Calculate f_cost (total cost)
        f_cost = g_cost + h_cost
        
        return f_cost
    
    def calculate_g_cost(self, node):
        # Implement actual distance calculation based on your node structure
        # This is a placeholder implementation
        return 0
    
    def calculate_h_cost(self, node):
        # Implement heuristic calculation (e.g., Euclidean distance, Manhattan distance)
        # This is a placeholder implementation
        return 0