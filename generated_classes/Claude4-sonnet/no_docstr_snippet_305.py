class OverrideCheck:
    def __init__(self, func, expected_parent_cls):
        self.func = func
        self.expected_parent_cls = expected_parent_cls
        self.name = None

    def __set_name__(self, owner, name):
        self.name = name
        
        # Check if the method exists in the expected parent class
        if not hasattr(self.expected_parent_cls, name):
            raise AttributeError(f"Method '{name}' does not exist in {self.expected_parent_cls.__name__}")
        
        # Check if the owner class actually inherits from the expected parent
        if not issubclass(owner, self.expected_parent_cls):
            raise TypeError(f"Class {owner.__name__} does not inherit from {self.expected_parent_cls.__name__}")
        
        # Set the actual method on the owner class
        setattr(owner, name, self.func)