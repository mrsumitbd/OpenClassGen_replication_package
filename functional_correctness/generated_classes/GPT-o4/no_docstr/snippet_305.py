class OverrideCheck:
    def __init__(self, func, expected_parent_cls):
        self.func = func
        self.expected_parent_cls = expected_parent_cls

    def __set_name__(self, owner, name):
        if not issubclass(owner, self.expected_parent_cls):
            raise TypeError(
                f"{owner.__name__!r} is not a subclass of {self.expected_parent_cls.__name__!r}"
            )
        if not hasattr(self.expected_parent_cls, name):
            raise TypeError(
                f"Method {name!r} does not override any method of "
                f"{self.expected_parent_cls.__name__!r}"
            )

    def __get__(self, instance, owner):
        return self.func.__get__(instance, owner)