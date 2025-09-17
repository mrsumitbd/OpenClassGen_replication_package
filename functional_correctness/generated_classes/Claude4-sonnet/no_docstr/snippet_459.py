class ModuleMock(object):
    def __init__(self, *args, **kwargs):
        self._name = kwargs.get('_name', 'ModuleMock')
        self._children = {}
        for key, value in kwargs.items():
            if not key.startswith('_'):
                setattr(self, key, value)

    def __call__(self, *args, **kwargs):
        return ModuleMock(_name=f"{self._name}()")

    def __iter__(self):
        return iter([])

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
        
        if name not in self._children:
            self._children[name] = ModuleMock(_name=f"{self._name}.{name}")
        return self._children[name]

    @classmethod
    def __getattr__(cls, name):
        return ModuleMock(_name=name)