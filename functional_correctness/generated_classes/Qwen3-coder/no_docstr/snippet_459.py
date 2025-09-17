class ModuleMock(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return ModuleMock()

    def __iter__(self):
        return iter([])

    @classmethod
    def __getattr__(cls, name):
        return ModuleMock()