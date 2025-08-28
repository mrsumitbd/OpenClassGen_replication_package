class Plane:
    def __init__(self, normal, p):
        '''
        Equation of a plane, in the form n.x+p = 0
        :param Vector normal:
        :param float p:
        :return:
        '''
        self.normal = normal
        self.p = p

    def __str__(self):
        return f"Plane(normal={self.normal}, p={self.p})"

    def perpendicular_distance_to_point(self, other):
        '''
        Calculate the perpendicular distance of a point from a place
        :param Point other:
        :return:
        '''
        return abs(self.normal.dot(other) + self.p) / self.normal.magnitude()

    def line_of_intersection(self, other):
        '''
        Find the line of intersection between two planes
        :param Plane other:
        :return Line:
        '''
        direction = self.normal.cross(other.normal)
        
        # Find a point on the line of intersection
        # We need to solve the system of equations:
        # n1.x + p1 = 0
        # n2.x + p2 = 0
        
        # Find the coordinate with the largest component in the direction vector
        abs_dir = [abs(direction.x), abs(direction.y), abs(direction.z)]
        max_index = abs_dir.index(max(abs_dir))
        
        if max_index == 0:  # x component is largest
            # Set x = 0, solve for y and z
            det = self.normal.y * other.normal.z - self.normal.z * other.normal.y
            y = (self.normal.z * other.p - other.normal.z * self.p) / det
            z = (other.normal.y * self.p - self.normal.y * other.p) / det
            point = Point(0, y, z)
        elif max_index == 1:  # y component is largest
            # Set y = 0, solve for x and z
            det = self.normal.x * other.normal.z - self.normal.z * other.normal.x
            x = (self.normal.z * other.p - other.normal.z * self.p) / det
            z = (other.normal.x * self.p - self.normal.x * other.p) / det
            point = Point(x, 0, z)
        else:  # z component is largest
            # Set z = 0, solve for x and y
            det = self.normal.x * other.normal.y - self.normal.y * other.normal.x
            x = (self.normal.y * other.p - other.normal.y * self.p) / det
            y = (other.normal.x * self.p - self.normal.x * other.p) / det
            point = Point(x, y, 0)
        
        return Line(point, direction)