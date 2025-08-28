class Point:
    '''
    Represents a waypoint
    '''
    def __init__(self, parent_route):
        self.parent_route = parent_route

    def __repr__(self):
        return f"Point(parent_route={self.parent_route!r})"