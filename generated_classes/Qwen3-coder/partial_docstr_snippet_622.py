class GaussianMap(object):
    ''' Generate Gaussian weighted deformation map'''

    def __init__(self, image_shape, sigma=0.5):
        self.image_shape = image_shape
        self.sigma = sigma
        self.sigma_squared = sigma * sigma

    def get_gaussian_weight(self, anchor):
        '''
        Args:
            anchor: coordinate of the center
        '''
        # Create coordinate grids
        coords = np.ogrid[0:self.image_shape[0], 0:self.image_shape[1]]
        y_coords, x_coords = coords[0], coords[1]
        
        # Calculate squared distances from anchor point
        dy = y_coords - anchor[0]
        dx = x_coords - anchor[1]
        distance_squared = dy**2 + dx**2
        
        # Calculate Gaussian weights
        weights = np.exp(-distance_squared / (2 * self.sigma_squared))
        
        return weights