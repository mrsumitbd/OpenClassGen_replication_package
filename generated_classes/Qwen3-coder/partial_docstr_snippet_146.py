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
        self.saved_values = {}

    def __enter__(self):
        # Save current values of keys that exist in context
        for key in self.keys:
            if key in self.context:
                self.saved_values[key] = self.context[key]
        return self.context

    def __exit__(self, type, value, traceback):
        # Remove keys from context
        for key in self.keys:
            if key in self.context:
                del self.context[key]
        
        # Restore previously saved values if they existed
        for key, value in self.saved_values.items():
            self.context[key] = value