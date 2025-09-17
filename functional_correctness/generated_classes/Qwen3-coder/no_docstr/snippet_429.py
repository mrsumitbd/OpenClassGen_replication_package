class TouchUp:
    _registry = {}

    @classmethod
    def run(cls, app):
        if app in cls._registry:
            for target, method_name in cls._registry[app]:
                method = getattr(target, method_name)
                method()

    @classmethod
    def register(cls, target, method_name):
        app = getattr(target, '__app__', None)
        if app is None:
            raise ValueError("Target must have an '__app__' attribute")
        
        if app not in cls._registry:
            cls._registry[app] = []
        
        cls._registry[app].append((target, method_name))