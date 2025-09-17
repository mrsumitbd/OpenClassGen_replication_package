class SpawningProxy(object):
    def __init__(self, items, abort_on_error=False):
        self._items = list(items)
        self._abort_on_error = abort_on_error

    def __getattr__(self, name):
        def spawning_method(*args, _name=name, **kwargs):
            threads = []
            results = [None] * len(self._items)

            def call(idx, item):
                try:
                    results[idx] = getattr(item, _name)(*args, **kwargs)
                except Exception:
                    if self._abort_on_error:
                        raise
                    # swallow if not abort_on_error

            for idx, item in enumerate(self._items):
                gt = eventlet.spawn(call, idx, item)
                threads.append(gt)

            if self._abort_on_error:
                for gt in threads:
                    try:
                        gt.wait()
                    except Exception:
                        for t in threads:
                            if t is not gt:
                                try:
                                    t.kill()
                                except Exception:
                                    pass
                        raise
            else:
                for gt in threads:
                    try:
                        gt.wait()
                    except Exception:
                        pass

            return results

        return spawning_method