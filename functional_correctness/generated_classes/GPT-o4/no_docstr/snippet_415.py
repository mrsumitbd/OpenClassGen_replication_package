class InstanceHooks(object):
    def __init__(self, instance):
        self._instance = instance

    def _iter_funcs(self, func_name):
        inst = self._instance
        hook = getattr(inst, func_name, None)
        if hook is None:
            return
        if callable(hook):
            yield hook
        elif isinstance(hook, (list, tuple)):
            for fn in hook:
                if callable(fn):
                    yield fn

    def __getattr__(self, name):
        inst = self._instance
        attr = getattr(inst, name)
        if callable(attr):
            def wrapped(*args, **kwargs):
                for fn in self._iter_funcs(f'before_{name}'):
                    fn(*args, **kwargs)
                result = attr(*args, **kwargs)
                for fn in self._iter_funcs(f'after_{name}'):
                    fn(*args, **kwargs)
                return result
            return wrapped
        return attr