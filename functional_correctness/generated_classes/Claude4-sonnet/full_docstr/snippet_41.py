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
        if not hasattr(n, '__class__') or n.__class__.__name__ != 'Direction':
            raise ValueError("n must be a Direction object")
        if not hasattr(x0, '__class__') or x0.__class__.__name__ != 'Point':
            raise ValueError("x0 must be a Point object")
        if len(n) != 3:
            raise ValueError("Normal vector must be 3D")
        if len(x0) != 3:
            raise ValueError("Point must be 3D")
        
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
        if not hasattr(point_cloud, '__class__') or point_cloud.__class__.__name__ != 'PointCloud':
            raise ValueError("Input must be a PointCloud object")
        
        above_points = []
        below_points = []
        
        for point in point_cloud:
            diff = point - self.x0
            dot_product = self.n.dot(diff)
            
            if dot_product > 0:
                above_points.append(point)
            else:
                below_points.append(point)
        
        PointCloud = point_cloud.__class__
        return (PointCloud(above_points), PointCloud(below_points))