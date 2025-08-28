class requirekwargs:
    def __init__(self, *args):
        self._required = set(args)

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            missing = self._required - set(kwargs)
            if missing:
                name = f.__name__
                missing_list = ", ".join(sorted(missing))
                raise TypeError(f"{name}() missing required keyword arguments: {missing_list}")
            return f(*args, **kwargs)
        return wrapper