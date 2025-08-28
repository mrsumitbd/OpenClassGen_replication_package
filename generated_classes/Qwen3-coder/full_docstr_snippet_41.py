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
        if not hasattr(n, 'dimension') or n.dimension != 3:
            raise ValueError("Normal vector must be 3-dimensional")
        if not hasattr(x0, 'dimension') or x0.dimension != 3:
            raise ValueError("Point must be 3-dimensional")
        
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
        if not hasattr(point_cloud, 'points'):
            raise ValueError("Input must be a PointCloud")
        
        above_points = []
        below_points = []
        
        for point in point_cloud.points:
            # Calculate the dot product of (point - x0) with the normal vector
            # This gives us the signed distance from the point to the plane
            diff = [point[i] - self.x0[i] for i in range(3)]
            dot_product = sum(diff[i] * self.n[i] for i in range(3))
            
            if dot_product > 0:
                above_points.append(point)
            else:
                below_points.append(point)
        
        # Create new PointCloud objects (assuming PointCloud constructor takes a list of points)
        above_cloud = type(point_cloud)(above_points)
        below_cloud = type(point_cloud)(below_points)
        
        return (above_cloud, below_cloud)