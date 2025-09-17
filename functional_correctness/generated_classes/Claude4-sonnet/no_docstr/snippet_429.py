class TouchUp:
    _registered_methods = {}

    @classmethod
    def run(cls, app):
        for target, method_name in cls._registered_methods.items():
            if hasattr(target, method_name):
                method = getattr(target, method_name)
                if callable(method):
                    method(app)

    @classmethod
    def register(cls, target, method_name):
        cls._registered_methods[target] = method_name