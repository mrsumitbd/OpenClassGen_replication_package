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
        from past.translation import remove_hooks
        self.hooks_were_installed = hasattr(remove_hooks, '__call__')
        if self.hooks_were_installed:
            remove_hooks()
        return self

    def __exit__(self, *args):
        if self.hooks_were_installed:
            from past.translation import install_hooks
            install_hooks()