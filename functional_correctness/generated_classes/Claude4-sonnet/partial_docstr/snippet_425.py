class Point:
    '''
    Represents a waypoint
    '''

    def __init__(self, parent_route):
        self.parent_route = parent_route
        self.x = 0
        self.y = 0
        self.name = ""

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y}, name='{self.name}')"