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
    _used_backend = None

    def __init__(self, backend=""):
        '''Initialize context manager.'''
        self.backend = backend

    def __enter__(self):
        '''Enter context manager.'''
        self.ip = get_ipython()
        if self.ip is None:
            raise RuntimeError("interactive_backend can only be used in IPython environments")
        prev = matplotlib.get_backend()
        self._was_inline = "inline" in prev.lower()
        if not self._was_inline:
            raise RuntimeError("interactive_backend only supports inline -> interactive transitions")
        if interactive_backend._used_backend is None:
            # first use
            if self.backend:
                to_use = self.backend
                self.ip.run_line_magic("matplotlib", to_use)
                interactive_backend._used_backend = to_use
            else:
                # let IPython pick default interactive
                self.ip.run_line_magic("matplotlib", "")
                # detect actual and map to magic alias
                be = matplotlib.get_backend().lower()
                if "qt5" in be:
                    alias = "qt5"
                elif "qt4" in be:
                    alias = "qt4"
                elif "tk" in be:
                    alias = "tk"
                elif "wx" in be:
                    alias = "wx"
                elif "osx" in be:
                    alias = "osx"
                elif "gtk3" in be:
                    alias = "gtk3"
                else:
                    alias = be
                interactive_backend._used_backend = alias
        else:
            # subsequent use
            if self.backend and self.backend != interactive_backend._used_backend:
                raise ValueError(
                    f"Backend '{interactive_backend._used_backend}' was already chosen; "
                    f"cannot switch to '{self.backend}'"
                )
            self.ip.run_line_magic("matplotlib", interactive_backend._used_backend)
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        '''Exit context manager.'''
        if self._was_inline:
            self.ip.run_line_magic("matplotlib", "inline")