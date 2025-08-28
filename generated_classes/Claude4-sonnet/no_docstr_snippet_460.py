class requirekwargs:
    def __init__(self, *args):
        self.required_kwargs = set(args)

    def __call__(self, f):
        def wrapper(*args, **kwargs):
            missing_kwargs = self.required_kwargs - set(kwargs.keys())
            if missing_kwargs:
                raise TypeError(f"Missing required keyword arguments: {', '.join(sorted(missing_kwargs))}")
            return f(*args, **kwargs)
        return wrapper