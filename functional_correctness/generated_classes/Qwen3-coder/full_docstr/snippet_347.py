class interactive_backend:
    '''Context manager to change backend temporarily in ipython sesson.

    It uses ipython magic to change temporarily from the ipython inline backend to
    an interactive backend of choice. It cannot be used outside ipython sessions nor
    to change backends different than inline -> interactive.

    Notes
    -----
    The first time ``interactive_backend`` context manager is called, any of the available
    interactive backends can be chosen. The following times, this same backend must be used
    unless the kernel is restarted.

    Parameters
    ----------
    backend : str, optional
        Interactive backend to use. It will be passed to ``%matplotlib`` magic, refer to
        its docs to see available options.

    Examples
    --------
    Inside an ipython session (i.e. a jupyter notebook) with the inline backend set:

    .. code::

        >>> import arviz as az
        >>> idata = az.load_arviz_data("centered_eight")
        >>> az.plot_posterior(idata) # inline
        >>> with az.interactive_backend():
        ...     az.plot_density(idata) # interactive
        >>> az.plot_trace(idata) # inline

    '''

    def __init__(self, backend=""):
        '''Initialize context manager.'''
        self.backend = backend
        self.ipyshell = None
        self.original_backend = None

    def __enter__(self):
        '''Enter context manager.'''
        try:
            from IPython import get_ipython
        except ImportError:
            raise RuntimeError("interactive_backend can only be used within IPython sessions")
        
        self.ipyshell = get_ipython()
        if self.ipyshell is None:
            raise RuntimeError("interactive_backend can only be used within IPython sessions")
        
        # Get current backend
        try:
            current_backend = self.ipyshell.magic("matplotlib inline --list") or "inline"
        except:
            current_backend = "inline"
        
        self.original_backend = current_backend
        
        # Set the interactive backend
        if self.backend:
            self.ipyshell.magic(f"matplotlib {self.backend}")
        else:
            self.ipyshell.magic("matplotlib")
        
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        '''Exit context manager.'''
        if self.ipyshell is not None and self.original_backend is not None:
            if self.original_backend == "inline":
                self.ipyshell.magic("matplotlib inline")
            else:
                self.ipyshell.magic(f"matplotlib {self.original_backend}")