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
        if no_display:
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        self.plt = plt
        self.fig, self.ax = plt.subplots()
        self.no_display = no_display

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
        # Expecting atDataset._results to be a dict mapping method names
        # to tuples/lists (taus, values, [errors])
        if not hasattr(atDataset, '_results'):
            raise AttributeError("Dataset has no '_results' attribute; run compute() first")
        for name, data in atDataset._results.items():
            # data: (taus, values) or (taus, values, errors)
            taus = data[0]
            vals = data[1]
            errs = data[2] if (errorbars and len(data) > 2) else None

            if errorbars and errs is not None:
                self.ax.errorbar(taus, vals, yerr=errs, label=name, **kwargs)
            else:
                self.ax.plot(taus, vals, label=name, **kwargs)

        # log-log by default for Allan-type plots
        self.ax.set_xscale('log')
        self.ax.set_yscale('log')

        # Labels
        self.ax.set_xlabel('Tau')
        self.ax.set_ylabel('Allan deviation')

        if grid:
            self.ax.grid(True)

        self.ax.legend()

    def show(self):
        '''Calls matplotlib.pyplot.show()

            Keeping this separated from ``plot()`` allows to tweak display before
            rendering
        '''
        self.plt.show()

    def save(self, f):
        '''Save figure to file'''
        self.fig.savefig(f)