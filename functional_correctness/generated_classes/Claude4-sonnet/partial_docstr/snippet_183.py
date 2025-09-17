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
        import sys
        self.hooks_were_installed = hasattr(sys.meta_path[0], '__name__') and sys.meta_path[0].__name__ == 'past.translation'
        if self.hooks_were_installed:
            self.hook = sys.meta_path.pop(0)
        return self

    def __exit__(self, *args):
        import sys
        if self.hooks_were_installed:
            sys.meta_path.insert(0, self.hook)