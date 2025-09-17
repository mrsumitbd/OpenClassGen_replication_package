class _IffHasDelegate(object):
    '''Implements a conditional property using the descriptor protocol.
    Using this class to create a decorator will raise an ``AttributeError``
    if none of the delegates (specified in ``delegate_names``) is an attribute
    of the base object or the first found delegate does not have an attribute
    ``attribute_name``.

    This allows ducktyping of the decorated method based on
    ``delegate.attribute_name``. Here ``delegate`` is the first item in
    ``delegate_names`` for which ``hasattr(object, delegate) is True``.

    See https://docs.python.org/3/howto/descriptor.html for an explanation of
    descriptors.
    '''

    def __init__(self, fn, delegate_names):
        self.fn = fn
        self.delegate_names = delegate_names
        self.attribute_name = fn.__name__

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        
        # Find the first delegate that exists on the object
        delegate = None
        for delegate_name in self.delegate_names:
            if hasattr(obj, delegate_name):
                delegate = getattr(obj, delegate_name)
                break
        
        # Raise AttributeError if no delegate found
        if delegate is None:
            raise AttributeError(
                f"None of the delegates {self.delegate_names} found on object"
            )
        
        # Raise AttributeError if delegate doesn't have the required attribute
        if not hasattr(delegate, self.attribute_name):
            raise AttributeError(
                f"Delegate {delegate} does not have attribute {self.attribute_name}"
            )
        
        # Return the attribute from the delegate
        return getattr(delegate, self.attribute_name)