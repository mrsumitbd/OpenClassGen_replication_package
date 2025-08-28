class LogWrapper(object):
    def __init__(self, context):
        self._context = context

    def __call__(self, key, value):
        """
        Store a key/value pair in the wrapped context.
        Returns self to allow chaining.
        """
        try:
            # if context supports item assignment (e.g. dict)
            self._context[key] = value
        except Exception:
            # fallback to attribute assignment
            setattr(self._context, key, value)
        return self

    def __getattr__(self, name):
        """
        First try to get an item from the wrapped context (if it's a mapping),
        otherwise delegate attribute access to the context object.
        """
        # try item access
        try:
            return self._context[name]
        except Exception:
            # fallback to attribute access
            return getattr(self._context, name)