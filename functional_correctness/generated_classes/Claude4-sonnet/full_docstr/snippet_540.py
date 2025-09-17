class TimeSeries(object):
    '''A simple Base Class for various data sets.

    .. doctest::

        >>> from spectrum import TimeSeries
        >>> data = [1, 2, 3, 4, 3, 2, 1, 0 ]
        >>> ts = TimeSeries(data, sampling=1)
        >>> ts.plot()
        >>> ts.dt
        1.0

    '''

    def __init__(self, data, sampling=1):
        '''

        :param array data: input data (list or numpy.array)
        :param sampling: the sampling frequency of the data (default 1Hz)

        '''
        self.data = np.array(data)
        self.sampling = sampling
        self.dt = 1.0 / sampling

    def plot(self, **kargs):
        '''Plot the data set, using the sampling information to set the x-axis
        correctly.'''
        N = len(self.data)
        time_axis = np.arange(N) * self.dt
        plt.plot(time_axis, self.data, **kargs)
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.show()