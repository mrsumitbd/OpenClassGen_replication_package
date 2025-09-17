class KeepContext:
    '''
    Context manager that receives a `django.template.Context` instance and a list of keys

    Once the context manager is exited, it removes `keys` from the context, to avoid
    side effects in later layout objects that may use the same context variables.

    Layout objects should use `extra_context` to introduce context variables, never
    touch context object themselves, that could introduce side effects.
    '''

    def __init__(self, context, keys):
        self.context = context
        self.keys = keys

    def __enter__(self):
        return self.context

    def __exit__(self, exc_type, exc_value, traceback):
        for key in self.keys:
            try:
                del self.context[key]
            except (KeyError, AttributeError):
                # If the context doesn’t support deletion or key is missing, ignore
                pass
        return False