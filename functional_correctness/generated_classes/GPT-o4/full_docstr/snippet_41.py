class Plane3D(object):
    '''A plane in three dimensions.'''

    def __init__(self, n, x0):
        '''Initialize a plane with a normal vector and a point.

        Parameters
        ----------
        n : :obj:`Direction`
            A 3D normal vector to the plane.

        x0 : :obj:`Point`
            A 3D point in the plane.

        Raises
        ------
        ValueError
            If the parameters are of the wrong type or are not of dimension 3.
        '''
        # Type checks
        from collections.abc import Sequence

        if not isinstance(n, Direction):
            raise ValueError("n must be a Direction")
        if not isinstance(x0, Point):
            raise ValueError("x0 must be a Point")

        # Dimension checks
        try:
            ln = len(n)
        except Exception:
            raise ValueError("n must be a sequence of length 3")
        try:
            lx0 = len(x0)
        except Exception:
            raise ValueError("x0 must be a sequence of length 3")

        if ln != 3 or lx0 != 3:
            raise ValueError("n and x0 must both be 3-dimensional")

        self.n = n
        self.x0 = x0

    def split_points(self, point_cloud):
        '''Split a point cloud into two along this plane.

        Parameters
        ----------
        point_cloud : :obj:`PointCloud`
            The PointCloud to divide in two.

        Returns
        -------
        :obj:`tuple` of :obj:`PointCloud`
            Two new PointCloud objects. The first contains points above the
            plane, and the second contains points below the plane.

        Raises
        ------
        ValueError
            If the input is not a PointCloud.
        '''
        # Validate input
        if not isinstance(point_cloud, PointCloud):
            raise ValueError("point_cloud must be a PointCloud")

        above_pts = []
        below_pts = []

        # Helper for dot product
        def dot(u, v):
            return sum(ui * vi for ui, vi in zip(u, v))

        # For each point, compute signed distance by dot(n, p - x0)
        for p in point_cloud:
            if not isinstance(p, Point):
                raise ValueError("All elements of point_cloud must be Point instances")
            # Compute p - x0
            diff = [pi - xi for pi, xi in zip(p, self.x0)]
            val = dot(self.n, diff)
            if val >= 0:
                above_pts.append(p)
            else:
                below_pts.append(p)

        # Build new PointClouds
        top_cloud = PointCloud(above_pts)
        bottom_cloud = PointCloud(below_pts)
        return top_cloud, bottom_cloud