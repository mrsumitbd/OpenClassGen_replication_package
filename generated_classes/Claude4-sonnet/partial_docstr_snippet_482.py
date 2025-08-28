class PSFMoffat(object):
    '''Moffat PSF.'''

    def __init__(self, fwhm, moffat_beta):
        '''
        :param fwhm: full width at half maximum seeing condition
        :param moffat_beta: float, beta parameter of Moffat profile
        '''
        self.fwhm = fwhm
        self.moffat_beta = moffat_beta
        self.alpha = fwhm / (2 * np.sqrt(2**(1/moffat_beta) - 1))

    def displace_psf(self, x, y):
        '''
        :param x: x-coordinate of light ray
        :param y: y-coordinate of light ray
        :return: x', y' displaced by the two-dimensional PSF distribution function
        '''
        # Generate random displacement based on Moffat profile
        # Use rejection sampling or Box-Muller transform with Moffat distribution
        r = np.sqrt(x**2 + y**2)
        
        # Generate random radius from Moffat distribution
        u = np.random.uniform(0, 1, size=np.shape(x))
        r_new = self.alpha * np.sqrt((1 - u)**(-1/(self.moffat_beta - 0.5)) - 1)
        
        # Generate random angle
        theta = np.random.uniform(0, 2*np.pi, size=np.shape(x))
        
        # Convert back to Cartesian coordinates
        x_new = r_new * np.cos(theta)
        y_new = r_new * np.sin(theta)
        
        return x + x_new, y + y_new

    def convolution_kernel(self, delta_pix, num_pix=21):
        '''Normalized convolution kernel.
        :param delta_pix: pixel scale of kernel
        :param num_pix: number of pixels per axis of the kernel
        :return: 2d numpy array of kernel
        '''
        center = num_pix // 2
        x = np.arange(num_pix) - center
        y = np.arange(num_pix) - center
        X, Y = np.meshgrid(x * delta_pix, y * delta_pix)
        
        kernel = self.convolution_kernel_grid(X, Y)
        kernel = kernel / np.sum(kernel)  # Normalize
        
        return kernel

    def convolution_kernel_grid(self, x, y):
        '''
        :param x: x-coordinate of light ray
        :param y: y-coordinate of light ray
        :return: psf value at x and y grid positions
        '''
        r_squared = x**2 + y**2
        alpha_squared = self.alpha**2
        
        # Moffat profile: I(r) = (beta-1)/(pi*alpha^2) * (1 + r^2/alpha^2)^(-beta)
        normalization = (self.moffat_beta - 1) / (np.pi * alpha_squared)
        profile = normalization * (1 + r_squared / alpha_squared)**(-self.moffat_beta)
        
        return profile