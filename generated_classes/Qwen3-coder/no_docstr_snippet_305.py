class OverrideCheck:
    def __init__(self, func, expected_parent_cls):
        self.func = func
        self.expected_parent_cls = expected_parent_cls
        self.name = func.__name__

    def __set_name__(self, owner, name):
        if not issubclass(owner, self.expected_parent_cls):
            raise TypeError(f"{owner.__name__} must inherit from {self.expected_parent_cls.__name__}")
        
        # Check if the method exists in the parent class
        if not hasattr(self.expected_parent_cls, self.name):
            raise TypeError(f"{self.name} is not defined in {self.expected_parent_cls.__name__}")
        
        # Check if the method is actually overridden
        if getattr(self.expected_parent_cls, self.name) is self.func:
            raise TypeError(f"{self.name} in {owner.__name__} does not override the parent method")
        
        # Set the function as an attribute of the owner class
        setattr(owner, name, self.func)