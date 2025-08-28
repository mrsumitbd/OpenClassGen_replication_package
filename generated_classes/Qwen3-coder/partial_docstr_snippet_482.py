class PSFMoffat(object):
    '''Moffat PSF.'''

    def __init__(self, fwhm, moffat_beta):
        '''

        :param fwhm: full width at half maximum seeing condition
        :param moffat_beta: float, beta parameter of Moffat profile
        '''
        self.fwhm = fwhm
        self.beta = moffat_beta
        # Calculate alpha parameter from FWHM and beta
        self.alpha = fwhm / (2 * np.sqrt(2**(1/self.beta) - 1))

    def displace_psf(self, x, y):
        '''

        :param x: x-coordinate of light ray
        :param y: y-coordinate of light ray
        :return: x', y' displaced by the two-dimensional PSF distribution function
        '''
        # Generate random numbers for sampling
        r = np.random.random()
        theta = 2 * np.pi * np.random.random()
        
        # Inverse transform sampling for Moffat distribution
        # For radial distance sampling
        r_moffat = self.alpha * np.sqrt((1 - r)**(-1/self.beta) - 1)
        
        # Convert to Cartesian coordinates
        dx = r_moffat * np.cos(theta)
        dy = r_moffat * np.sin(theta)
        
        return x + dx, y + dy

    def convolution_kernel(self, delta_pix, num_pix=21):
        '''Normalized convolution kernel.

        :param delta_pix: pixel scale of kernel
        :param num_pix: number of pixels per axis of the kernel
        :return: 2d numpy array of kernel
        '''
        # Create coordinate grid
        center = (num_pix - 1) / 2
        x = np.arange(num_pix) * delta_pix - center * delta_pix
        y = np.arange(num_pix) * delta_pix - center * delta_pix
        xx, yy = np.meshgrid(x, y)
        
        # Calculate radial distance
        r = np.sqrt(xx**2 + yy**2)
        
        # Moffat profile
        kernel = (self.beta - 1) / (np.pi * self.alpha**2) * (1 + (r/self.alpha)**2)**(-self.beta)
        
        # Normalize kernel
        kernel = kernel / np.sum(kernel)
        
        return kernel

    def convolution_kernel_grid(self, x, y):
        '''
        :param x: x-coordinate of light ray
        :param y: y-coordinate of light ray
        :return: psf value at x and y grid positions
        '''
        # Calculate radial distance
        r = np.sqrt(x**2 + y**2)
        
        # Moffat profile
        psf_value = (self.beta - 1) / (np.pi * self.alpha**2) * (1 + (r/self.alpha)**2)**(-self.beta)
        
        return psf_value