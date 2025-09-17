class suspend_hooks(object):
    '''
    Acts as a context manager. Use like this:

    >>> from past import translation
    >>> translation.install_hooks()
    >>> import http.client
    >>> # ...
    >>> with translation.suspend_hooks():
    >>>     import requests     # or others that support Py2/3

    If the hooks were disabled before the context, they are not installed when
    the context is left.
    '''

    def __enter__(self):
        # Remember whether hooks are currently installed
        self._was_enabled = globals().get('HOOKS_ENABLED', False)
        if self._was_enabled:
            # Temporarily remove them
            remove_hooks()

    def __exit__(self, exc_type, exc_value, traceback):
        # Re-install only if they were enabled before entering
        if getattr(self, '_was_enabled', False):
            install_hooks()