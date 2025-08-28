class GaussianMap(object):
    ''' Generate Gaussian weighted deformation map'''

    def __init__(self, image_shape, sigma=0.5):
        self.image_shape = image_shape
        self.sigma = sigma
        h, w = image_shape[:2]
        ys = np.arange(h).reshape(h, 1)
        xs = np.arange(w).reshape(1, w)
        self.ys = np.tile(ys, (1, w))
        self.xs = np.tile(xs, (h, 1))

    def get_gaussian_weight(self, anchor):
        '''
        Args:
            anchor: coordinate of the center (row, col)
        '''
        y0, x0 = anchor
        dy2 = (self.ys - y0) ** 2
        dx2 = (self.xs - x0) ** 2
        exponent = -(dx2 + dy2) / (2 * (self.sigma ** 2))
        return np.exp(exponent)