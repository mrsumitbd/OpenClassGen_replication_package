class InstanceHooks(object):
    def __init__(self, instance):
        self.instance = instance

    def _iter_funcs(self, func_name):
        if hasattr(self.instance, '_hooks') and func_name in self.instance._hooks:
            for func in self.instance._hooks[func_name]:
                yield func

    def __getattr__(self, name):
        def hook_wrapper(*args, **kwargs):
            results = []
            for func in self._iter_funcs(name):
                result = func(*args, **kwargs)
                results.append(result)
            return results
        return hook_wrapper