class COGENOperationCall(object):
    def __init__(self, gate, obj):
        if not (callable(gate) or isinstance(gate, str)):
            raise TypeError("gate must be a callable or a string name")
        self.gate = gate
        self.obj = obj

    def __call__(self, *args, **kwargs):
        if callable(self.gate):
            return self.gate(self.obj, *args, **kwargs)
        else:
            method = getattr(self.obj, self.gate)
            if not callable(method):
                raise TypeError(f"Attribute '{self.gate}' of object is not callable")
            return method(*args, **kwargs)