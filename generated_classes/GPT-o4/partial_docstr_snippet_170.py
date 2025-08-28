class Plane:
    def __init__(self, normal, p):
        """
        Equation of a plane, in the form n.x + p = 0
        :param Vector normal:
        :param float p:
        """
        self.normal = normal
        self.p = float(p)

    def __str__(self):
        n = self.normal
        return f"{n.x}x + {n.y}y + {n.z}z + {self.p} = 0"

    def perpendicular_distance_to_point(self, other):
        """
        Calculate the perpendicular distance of a point from a plane
        :param Point other:
        """
        v = other.to_vector()
        num = abs(self.normal.dot(v) + self.p)
        den = self.normal.norm()
        return num / den

    def line_of_intersection(self, other):
        """
        Find the line of intersection between two planes
        :param Plane other:
        :return Line or None if parallel
        """
        n1 = self.normal
        n2 = other.normal
        d = n1.cross(n2)
        if d.norm() == 0:
            return None
        # point on line
        # equations: n1·r = -p1, n2·r = -p2
        p1 = -self.p
        p2 = -other.p
        temp = (n2 * p1) - (n1 * p2)
        num = temp.cross(d)
        denom = d.dot(d)
        point_vec = num * (1.0 / denom)
        point = Point(point_vec.x, point_vec.y, point_vec.z)
        return Line(point, d)