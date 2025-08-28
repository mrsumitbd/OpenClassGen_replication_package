class PSFMoffat(object):
    '''Moffat PSF.'''

    def __init__(self, fwhm, moffat_beta):
        '''
        :param fwhm: full width at half maximum seeing condition
        :param moffat_beta: float, beta parameter of Moffat profile
        '''
        self.fwhm = fwhm
        self.beta = moffat_beta
        self.alpha = fwhm / (2.0 * sqrt(2.0**(1.0/self.beta) - 1.0))
        self.norm = (self.beta - 1.0) / (pi * self.alpha**2)

    def displace_psf(self, x, y):
        '''
        :param x: x-coordinate of light ray
        :param y: y-coordinate of light ray
        :return: x', y' displaced by the two-dimensional PSF distribution function
        '''
        u = random()
        r = self.alpha * sqrt((1.0 - u)**(-1.0/(self.beta - 1.0)) - 1.0)
        theta = uniform(0.0, 2.0*pi)
        dx = r * cos(theta)
        dy = r * sin(theta)
        return x + dx, y + dy

    def convolution_kernel(self, delta_pix, num_pix=21):
        '''Normalized convolution kernel.

        :param delta_pix: pixel scale of kernel
        :param num_pix: number of pixels per axis of the kernel
        :return: 2d numpy array of kernel
        '''
        half = num_pix // 2
        coords = (np.arange(num_pix) - half) * delta_pix
        X, Y = np.meshgrid(coords, coords)
        K = self.convolution_kernel_grid(X, Y)
        return K / np.sum(K)

    def convolution_kernel_grid(self, x, y):
        '''
        :param x: x-coordinate of light ray
        :param y: y-coordinate of light ray
        :return: psf value at x and y grid positions
        '''
        r2 = x**2 + y**2
        return self.norm * (1.0 + r2 / self.alpha**2)**(-self.beta)