class TouchUp:
    _registry = []

    @classmethod
    def register(cls, target, method_name):
        """
        Register a callback method by specifying the target (object or class)
        and the name of the method (string) to be called later.
        """
        cls._registry.append((target, method_name))

    @classmethod
    def run(cls, app):
        """
        Invoke all registered methods, passing the `app` argument to each.
        """
        for target, method_name in cls._registry:
            method = getattr(target, method_name, None)
            if callable(method):
                method(app)