class InstanceHooks(object):

    def __init__(self, instance):
        self.instance = instance

    def _iter_funcs(self, func_name):
        for cls in type(self.instance).__mro__:
            if hasattr(cls, func_name):
                yield getattr(cls, func_name)

    def __getattr__(self, name):
        def hook_caller(*args, **kwargs):
            results = []
            for func in self._iter_funcs(name):
                result = func(self.instance, *args, **kwargs)
                results.append(result)
            return results
        return hook_caller