class Plot(object):
    ''' A class for plotting data once computed by Allantools

    :Example:
        ::

            import allantools
            import numpy as np
            a = allantools.Dataset(data=np.random.rand(1000))
            a.compute("mdev")
            b = allantools.Plot()
            b.plot(a)
            b.show()

    Uses matplotlib. self.fig and self.ax stores the return values of
    matplotlib.pyplot.subplots(). plot() sets various defaults, but you
    can change them by using standard matplotlib method on self.fig and self.ax
    '''

    def __init__(self, no_display=False):
        ''' set ``no_display`` to ``True`` when we don't have an X-window
        (e.g. for tests)
        '''
        self.no_display = no_display
        if no_display:
            import matplotlib
            matplotlib.use('Agg')
        self.fig = None
        self.ax = None

    def plot(self, atDataset,
             errorbars=False,
             grid=False,
             **kwargs):
        ''' Use matplotlib methods for plotting

        Additional keywords arguments are passed to
        :py:func:`matplotlib.pyplot.plot`.

        Parameters
        ----------
        atDataset : allantools.Dataset()
            a dataset with computed data
        errorbars : boolean
            Plot errorbars. Defaults to False
        grid : boolean
            Plot grid. Defaults to False

        '''
        self.fig, self.ax = plt.subplots()
        
        if errorbars and hasattr(atDataset, 'dev_err') and atDataset.dev_err is not None:
            self.ax.errorbar(atDataset.tau, atDataset.dev, yerr=atDataset.dev_err, 
                           **kwargs)
        else:
            self.ax.plot(atDataset.tau, atDataset.dev, **kwargs)
            
        self.ax.set_xscale('log')
        self.ax.set_yscale('log')
        
        if grid:
            self.ax.grid(True)
            
        self.ax.set_xlabel('Tau')
        self.ax.set_ylabel('Deviation')

    def show(self):
        '''Calls matplotlib.pyplot.show()

        Keeping this separated from ``plot()`` allows to tweak display before
        rendering
        '''
        if self.fig is not None:
            plt.show()

    def save(self, f):
        '''Save figure to file
        '''
        if self.fig is not None:
            self.fig.savefig(f)