class GaussianMap(object):
    ''' Generate Gaussian weighted deformation map'''

    def __init__(self, image_shape, sigma=0.5):
        self.image_shape = image_shape
        self.sigma = sigma
        self.height, self.width = image_shape[:2]
        
        # Create coordinate grids
        y_coords, x_coords = np.meshgrid(np.arange(self.height), np.arange(self.width), indexing='ij')
        self.coords = np.stack([y_coords, x_coords], axis=-1)

    def get_gaussian_weight(self, anchor):
        '''
        Args:
            anchor: coordinate of the center
        '''
        anchor = np.array(anchor)
        
        # Calculate squared distances from anchor point
        distances_sq = np.sum((self.coords - anchor) ** 2, axis=-1)
        
        # Calculate Gaussian weights
        weights = np.exp(-distances_sq / (2 * self.sigma ** 2))
        
        return weights