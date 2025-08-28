class Plane:
    def __init__(self, normal, p):
        '''
        Equation of a plane, in the form n.x + p = 0
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
        Calculate the perpendicular distance of a point from a plane
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
        from line import Line
        from vector import Vector
        
        # Direction of the line is the cross product of the normals
        direction = self.normal.cross(other.normal)
        
        # If direction is zero, planes are parallel
        if direction.magnitude() == 0:
            raise ValueError("Planes are parallel, no intersection line")
        
        # Find a point on the line by solving the system of equations
        # We solve: n1.x + p1 = 0 and n2.x + p2 = 0
        # Set one coordinate to 0 and solve for the other two
        n1, n2 = self.normal, other.normal
        p1, p2 = self.p, other.p
        
        # Try setting z = 0 first
        det = n1.x * n2.y - n1.y * n2.x
        if det != 0:
            x = (n1.y * p2 - n2.y * p1) / det
            y = (n2.x * p1 - n1.x * p2) / det
            point = Vector(x, y, 0)
        else:
            # Try setting y = 0
            det = n1.x * n2.z - n1.z * n2.x
            if det != 0:
                x = (n1.z * p2 - n2.z * p1) / det
                z = (n2.x * p1 - n1.x * p2) / det
                point = Vector(x, 0, z)
            else:
                # Try setting x = 0
                det = n1.y * n2.z - n1.z * n2.y
                if det != 0:
                    y = (n1.z * p2 - n2.z * p1) / det
                    z = (n2.y * p1 - n1.y * p2) / det
                    point = Vector(0, y, z)
                else:
                    raise ValueError("Cannot find intersection point")
        
        return Line(point, direction)