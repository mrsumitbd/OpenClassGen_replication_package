class COGENOperationCall(object):
    def __init__(self, gate, obj):
        self.gate = gate
        self.obj = obj

    def __call__(self, *args, **kwargs):
        return self.gate(self.obj, *args, **kwargs)