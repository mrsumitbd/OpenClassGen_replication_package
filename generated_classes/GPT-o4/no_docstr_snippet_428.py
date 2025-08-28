class GroupBySetup:
    def __init__(self, cache_dir='groupby_cache'):
        self.cache_dir = cache_dir
        self._lock = RLock()
        self._memory = {}
        os.makedirs(self.cache_dir, exist_ok=True)

    def setup_cache(self, key=None, func=None, use_disk=False):
        """
        If called with no arguments, clears both in-memory and on-disk cache.
        If called with key and func, computes func(), caches it under key and returns it.
        If use_disk=True, also writes to disk.
        """
        with self._lock:
            if key is None and func is None:
                # clear all caches
                self._memory.clear()
                for fname in os.listdir(self.cache_dir):
                    try:
                        os.remove(os.path.join(self.cache_dir, fname))
                    except OSError:
                        pass
                return

            if key in self._memory:
                return self._memory[key]

            path = os.path.join(self.cache_dir, f'{key!r}.pkl')
            if use_disk and os.path.exists(path):
                with open(path, 'rb') as f:
                    result = pickle.load(f)
                self._memory[key] = result
                return result

            # compute, cache in memory, optionally on disk
            result = func()
            self._memory[key] = result
            if use_disk:
                with open(path, 'wb') as f:
                    pickle.dump(result, f)
            return result

    def setup_cache(self):
        """
        Alias: clears both in-memory and on-disk cache.
        """
        return self.setup_cache(key=None, func=None)